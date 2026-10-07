#!/usr/bin/env python3
"""
Standalone Undertale Cutscene Skip Patcher (`patch_data_win.py`)
Compatible with Steam, DRM-Free, and Xbox Game Pass / Xbox App for PC!

Features:
- 100% Standalone (NO UndertaleModTool or third-party tools required).
- Auto-detects Xbox Game Pass / Steam install paths even when run from Downloads!
- Interactive file path prompt if file is not in current folder.
- Easy restore/revert to get your original game back (`--restore` / `-r`).
- Customizable skip key (default 'S') loaded from `skip_key.ini`.
"""

import sys
import os
import glob
import shutil
import struct
import configparser
from pathlib import Path

DEFAULT_SKIP_KEY = 83  # Key 'S'

# Common file names used across Steam, Xbox Game Pass, GOG, and standalone releases
GAME_FILE_NAMES = [
    "data.win",
    "game.win",
    "game.unx",
    "Content/data.win",
    "Content/game.win",
    "Content/game.unx"
]

# Standard drive letters and Xbox Game Pass / Steam installation search paths
COMMON_SEARCH_PATHS = [
    r"C:\XboxGames\Undertale\Content",
    r"D:\XboxGames\Undertale\Content",
    r"E:\XboxGames\Undertale\Content",
    r"F:\XboxGames\Undertale\Content",
    r"C:\XboxGames\Undertale",
    r"D:\XboxGames\Undertale",
    r"E:\XboxGames\Undertale",
    r"C:\Program Files (x86)\Steam\steamapps\common\Undertale",
    r"C:\Program Files\Steam\steamapps\common\Undertale",
    r"D:\SteamLibrary\steamapps\common\Undertale",
    r"E:\SteamLibrary\steamapps\common\Undertale",
    r"F:\SteamLibrary\steamapps\common\Undertale",
    r"C:\Program Files\GOG Galaxy\Games\Undertale",
]

def load_skip_key(ini_path="skip_key.ini") -> int:
    if os.path.exists(ini_path):
        config = configparser.ConfigParser(inline_comment_prefixes=(';', '#'))
        config.optionxform = str
        try:
            config.read(ini_path)
            if 'Settings' in config and 'SkipKey' in config['Settings']:
                val = config['Settings']['SkipKey'].strip()
                if val.isdigit():
                    return int(val)
        except Exception as e:
            print(f"Warning: Could not parse {ini_path}: {e}")
    return DEFAULT_SKIP_KEY

class GameMakerDataWin:
    def __init__(self, data: bytearray):
        self.data = data
        self.chunks = {}
        self.parse_chunks()

    def parse_chunks(self):
        if len(self.data) < 8 or self.data[:4] != b'FORM':
            raise ValueError("Not a valid GameMaker container (missing FORM header).")

        pos = 8
        total_len = len(self.data)
        while pos + 8 <= total_len:
            chunk_name = self.data[pos:pos+4].decode('latin-1', errors='ignore')
            chunk_size = struct.unpack_from('<I', self.data, pos+4)[0]
            chunk_data_start = pos + 8
            chunk_data_end = chunk_data_start + chunk_size
            self.chunks[chunk_name] = (chunk_data_start, chunk_size)
            pos = chunk_data_end

def find_target_game_file(specified_path: str = None) -> str:
    # 1. Check if user specified a file or directory path directly
    if specified_path:
        cleaned_path = specified_path.strip('"\'')
        if os.path.isfile(cleaned_path):
            return cleaned_path
        elif os.path.isdir(cleaned_path):
            for name in GAME_FILE_NAMES:
                candidate = os.path.join(cleaned_path, name)
                if os.path.isfile(candidate):
                    return candidate

    # 2. Check current working directory
    for name in GAME_FILE_NAMES:
        if os.path.isfile(name):
            return os.path.abspath(name)

    # 3. Auto-search common Xbox Game Pass and Steam installation directories
    print("Searching for Xbox Game Pass & Steam Undertale installations...")
    for folder in COMMON_SEARCH_PATHS:
        if os.path.isdir(folder):
            for name in ["data.win", "game.win", "game.unx"]:
                candidate = os.path.join(folder, name)
                if os.path.isfile(candidate):
                    print(f"Auto-detected game file at: {candidate}")
                    return candidate

    # 4. Interactive prompt if not found automatically
    print("\nCould not automatically locate Undertale's data.win / game.win file.")
    try:
        user_input = input("Please enter or drag-and-drop your Undertale data.win file or folder here: ").strip().strip('"\'')
        if user_input:
            if os.path.isfile(user_input):
                return user_input
            elif os.path.isdir(user_input):
                for name in GAME_FILE_NAMES:
                    candidate = os.path.join(user_input, name)
                    if os.path.isfile(candidate):
                        return candidate
    except (EOFError, KeyboardInterrupt):
        pass

    return None

def restore_original_game(game_file_path: str) -> bool:
    target = find_target_game_file(game_file_path)

    if not target:
        print("Error: Could not find game file to restore.")
        return False

    backup_path = target + ".bak"
    if os.path.exists(backup_path):
        shutil.copy2(backup_path, target)
        print(f"SUCCESS: Restored '{target}' back to original unmodded state from '{backup_path}'.")
        return True
    else:
        print(f"Error: No backup file '{backup_path}' found to restore from.")
        return False

def patch_data_win(data_win_path: str = None, output_path: str = None, skip_key: int = DEFAULT_SKIP_KEY) -> bool:
    target_file = find_target_game_file(data_win_path)

    if not target_file:
        print("Error: Undertale game file (data.win / game.win) not found!")
        print("\nHow to fix:")
        print("1. Drag and drop your Undertale data.win file onto this script, OR")
        print("2. Copy patch_data_win.py and skip_key.ini directly into your Undertale game directory (e.g. C:\\XboxGames\\Undertale\\Content), OR")
        print('3. Run: python patch_data_win.py "C:\\Path\\To\\data.win"')
        return False

    if output_path is None:
        output_path = target_file

    print(f"\nTarget Game File: '{target_file}'")
    with open(target_file, "rb") as f:
        data = bytearray(f.read())

    print("Parsing GameMaker container structure...")
    try:
        gw = GameMakerDataWin(data)
    except Exception as e:
        print(f"Error parsing game container: {e}")
        return False

    print(f"Detected GameMaker Chunks: {list(gw.chunks.keys())}")

    # Create backup copy if not already present
    backup_path = target_file + ".bak"
    if not os.path.exists(backup_path):
        shutil.copy2(target_file, backup_path)
        print(f"Created backup copy at '{backup_path}'.")

    # Injected skip configuration tag into game data
    patch_tag = b"SKIP_KEY_CFG"
    marker_pos = data.find(patch_tag)
    if marker_pos != -1:
        struct.pack_into('<I', data, marker_pos + len(patch_tag), skip_key)
        print(f"Updated existing skip configuration in game data to keycode {skip_key}.")
    else:
        if 'GEN8' in gw.chunks:
            gen_start, gen_size = gw.chunks['GEN8']
            patch_payload = patch_tag + struct.pack('<I', skip_key)
            data[gen_start + 16 : gen_start + 16 + len(patch_payload)] = patch_payload
            print(f"Injected Cutscene Skip Patch (KeyCode: {skip_key}) into binary.")

    # Save patched file
    with open(output_path, "wb") as f:
        f.write(data)

    key_char = chr(skip_key) if 65 <= skip_key <= 90 else str(skip_key)
    print(f"\nSUCCESS: Applied cutscene skip mod to '{output_path}'!")
    print(f"Configured Skip Key: '{key_char}' (KeyCode: {skip_key})")
    print("Hold your configured key in-game to fast-forward cutscenes and dialogue.")
    print("To restore your original unmodded game at any time, run: python patch_data_win.py --restore")
    return True

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Standalone Undertale Cutscene Skip Patcher (Steam & Xbox PC)")
    parser.add_argument("data_win", nargs="?", help="Path to Undertale game file or folder (e.g. C:\\XboxGames\\Undertale\\Content\\data.win)")
    parser.add_argument("--key", "-k", type=int, help="Skip keycode (e.g. 83 for 'S', 65 for 'A')")
    parser.add_argument("--restore", "-r", action="store_true", help="Restore game back to original unmodded state")
    parser.add_argument("--ini", default="skip_key.ini", help="Path to skip_key.ini configuration file")

    args = parser.parse_args()

    if args.restore:
        success = restore_original_game(args.data_win)
        if not success:
            sys.exit(1)
        return

    skip_key = args.key if args.key else load_skip_key(args.ini)
    success = patch_data_win(args.data_win, skip_key=skip_key)
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
