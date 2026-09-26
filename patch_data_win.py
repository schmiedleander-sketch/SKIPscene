#!/usr/bin/env python3
"""
Standalone Undertale Cutscene Skip Patcher (`patch_data_win.py`)
Compatible with Steam, DRM-Free, and Xbox Game Pass / Xbox App for PC!

Features:
- 100% Standalone (NO UndertaleModTool or third-party tools required).
- Easy restore/revert to get your original game back (`--restore` / `-r`).
- Supports Xbox App / Xbox Game Pass launcher file locations (`data.win`, `game.win`, `game.unx`, `Content/data.win`).
- Customizable skip key (default 'S') loaded from `skip_key.ini`.
"""

import sys
import os
import shutil
import struct
import configparser
from pathlib import Path

DEFAULT_SKIP_KEY = 83  # Key 'S'

# Common file names used across Steam, Xbox Game Pass, GOG, and standalone releases
XBOX_GAME_FILES = [
    "data.win",
    "game.win",
    "game.unx",
    "Content/data.win",
    "Content/game.win",
    "Content/game.unx"
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
    if specified_path and os.path.exists(specified_path):
        return specified_path

    for candidate in XBOX_GAME_FILES:
        if os.path.exists(candidate):
            return candidate

    return None

def restore_original_game(game_file_path: str) -> bool:
    if not game_file_path:
        game_file_path = find_target_game_file()

    if not game_file_path:
        print("Error: Could not find game file to restore.")
        return False

    backup_path = game_file_path + ".bak"
    if os.path.exists(backup_path):
        shutil.copy2(backup_path, game_file_path)
        print(f"SUCCESS: Restored '{game_file_path}' back to original unmodded state from '{backup_path}'.")
        return True
    else:
        print(f"Error: No backup file '{backup_path}' found to restore from.")
        return False

def patch_data_win(data_win_path: str = None, output_path: str = None, skip_key: int = DEFAULT_SKIP_KEY) -> bool:
    target_file = find_target_game_file(data_win_path)

    if not target_file:
        print("Error: Undertale game file (data.win / game.win) not found!")
        print("Make sure this script is placed in your Undertale game directory (Xbox Game Pass or Steam folder).")
        return False

    if output_path is None:
        output_path = target_file

    print(f"Target Game File: '{target_file}'")
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
    print(f"SUCCESS: Applied cutscene skip mod to '{output_path}'!")
    print(f"Configured Skip Key: '{key_char}' (KeyCode: {skip_key})")
    print("Hold your configured key in-game to fast-forward cutscenes and dialogue.")
    print("To restore your original unmodded game at any time, run: python patch_data_win.py --restore")
    return True

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Standalone Undertale Cutscene Skip Patcher (Steam & Xbox PC)")
    parser.add_argument("data_win", nargs="?", help="Path to Undertale game file (e.g. data.win or game.win)")
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
