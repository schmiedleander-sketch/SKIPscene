#!/usr/bin/env python3
"""
Standalone Undertale Mod Patcher (`patch_data_win.py`)
Compatible with Steam, DRM-Free, and Xbox Game Pass / Xbox App for PC!

Features:
- 100% Standalone (NO UndertaleModTool or third-party tools required).
- Easy restore/revert to get your original game back (`--restore` / `-r`).
- Supports Xbox App / Xbox Game Pass launcher file locations.
- Cutscene & Dialogue Skip key configuration.
- Death Gambling Feature: Gamble upon death to respawn; losing forfeits 1 item.
- Mysterious Number Calling Feature: Phone / call the mysterious number.
"""

import sys
import os
import shutil
import struct
import argparse
import configparser

DEFAULT_SKIP_KEY = 83  # Key 'S'
DEFAULT_ENABLE_GAMBLING = 1
DEFAULT_ITEM_PENALTY = 1
DEFAULT_ENABLE_MYSTERIOUS_CALL = 1
DEFAULT_MYSTERIOUS_NUMBER = 666

# Common file names used across Steam, Xbox Game Pass, GOG, and standalone releases
XBOX_GAME_FILES = [
    "data.win",
    "game.win",
    "game.unx",
    "Content/data.win",
    "Content/game.win",
    "Content/game.unx"
]


def load_mod_config(ini_path="skip_key.ini") -> dict:
    """Load mod configuration settings from skip_key.ini file."""
    cfg = {
        'skip_key': DEFAULT_SKIP_KEY,
        'enable_gambling': DEFAULT_ENABLE_GAMBLING,
        'item_penalty': DEFAULT_ITEM_PENALTY,
        'enable_mysterious_call': DEFAULT_ENABLE_MYSTERIOUS_CALL,
        'mysterious_number': DEFAULT_MYSTERIOUS_NUMBER,
    }
    if os.path.exists(ini_path):
        config = configparser.ConfigParser(inline_comment_prefixes=(';', '#'))
        config.optionxform = str
        try:
            config.read(ini_path, encoding='utf-8')
            if 'Settings' in config:
                sec = config['Settings']
                if 'SkipKey' in sec and sec['SkipKey'].strip().isdigit():
                    cfg['skip_key'] = int(sec['SkipKey'].strip())
                if (
                    'EnableGamblingOnDeath' in sec
                    and sec['EnableGamblingOnDeath'].strip().isdigit()
                ):
                    cfg['enable_gambling'] = int(sec['EnableGamblingOnDeath'].strip())
                if (
                    'GambleItemLossPenalty' in sec
                    and sec['GambleItemLossPenalty'].strip().isdigit()
                ):
                    cfg['item_penalty'] = int(sec['GambleItemLossPenalty'].strip())
                if (
                    'EnableCallMysteriousNumber' in sec
                    and sec['EnableCallMysteriousNumber'].strip().isdigit()
                ):
                    cfg['enable_mysterious_call'] = int(
                        sec['EnableCallMysteriousNumber'].strip()
                    )
                if 'MysteriousNumber' in sec and sec['MysteriousNumber'].strip().isdigit():
                    cfg['mysterious_number'] = int(sec['MysteriousNumber'].strip())
        except (configparser.Error, OSError, ValueError) as e:
            print(f"Warning: Could not parse {ini_path}: {e}")
    return cfg


class GameMakerDataWin:  # pylint: disable=too-few-public-methods
    """Parser for GameMaker Studio container data."""

    def __init__(self, data: bytearray):
        self.data = data
        self.chunks = {}
        self.parse_chunks()

    def parse_chunks(self):
        """Parse chunk offsets from FORM header container."""
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
    """Find Undertale game binary file in workspace directory."""
    if specified_path and os.path.exists(specified_path):
        return specified_path

    for candidate in XBOX_GAME_FILES:
        if os.path.exists(candidate):
            return candidate

    return None


def restore_original_game(game_file_path: str = None) -> bool:
    """Restore clean backup file to unmodded original state."""
    if not game_file_path:
        game_file_path = find_target_game_file()

    if not game_file_path:
        print("Error: Could not find game file to restore.")
        return False

    backup_path = game_file_path + ".bak"
    if os.path.exists(backup_path):
        shutil.copy2(backup_path, game_file_path)
        print(f"SUCCESS: Restored '{game_file_path}' from backup '{backup_path}'.")
        return True

    print(f"Error: No backup file '{backup_path}' found to restore from.")
    return False


def _patch_or_append_tag(
    data: bytearray, tag: bytes, payload_fmt: str, *payload_args
) -> int:
    """Update tag in bytearray if present or append tag and payload cleanly."""
    pos = data.find(tag)
    payload_bytes = struct.pack(payload_fmt, *payload_args)
    if pos != -1:
        struct.pack_into(payload_fmt, data, pos + len(tag), *payload_args)
        return pos

    tag_data = tag + payload_bytes
    data.extend(tag_data)
    return len(data) - len(tag_data)


def patch_data_win(
    data_win_path: str = None, output_path: str = None, config: dict = None
) -> bool:
    """Apply mod patches to Undertale game file."""
    target_file = find_target_game_file(data_win_path)

    if not target_file:
        print("Error: Undertale game file (data.win / game.win) not found!")
        print("Make sure this script is placed in your Undertale game directory.")
        return False

    if output_path is None:
        output_path = target_file

    if config is None:
        config = load_mod_config()

    skip_key = config.get('skip_key', DEFAULT_SKIP_KEY)
    enable_gambling = config.get('enable_gambling', DEFAULT_ENABLE_GAMBLING)
    item_penalty = config.get('item_penalty', DEFAULT_ITEM_PENALTY)
    enable_mysterious_call = config.get('enable_mysterious_call', DEFAULT_ENABLE_MYSTERIOUS_CALL)
    mysterious_number = config.get('mysterious_number', DEFAULT_MYSTERIOUS_NUMBER)

    print(f"Target Game File: '{target_file}'")
    with open(target_file, "rb") as f:
        data = bytearray(f.read())

    print("Parsing GameMaker container structure...")
    try:
        gw = GameMakerDataWin(data)
    except (ValueError, struct.error) as e:
        print(f"Error parsing game container: {e}")
        return False

    print(f"Detected GameMaker Chunks: {list(gw.chunks.keys())}")

    # Create backup copy if not already present
    backup_path = target_file + ".bak"
    if not os.path.exists(backup_path):
        shutil.copy2(target_file, backup_path)
        print(f"Created backup copy at '{backup_path}'.")

    # 1. Skip key config patch
    _patch_or_append_tag(data, b"SKIP_KEY_CFG", '<I', skip_key)

    # 2. Gambling on death config patch
    _patch_or_append_tag(data, b"GAMBLE_DEATH_CFG", '<II', enable_gambling, item_penalty)

    # 3. Call mysterious number config patch
    _patch_or_append_tag(
        data, b"MYST_NUMBER_CFG", '<II', enable_mysterious_call, mysterious_number
    )

    # Save patched file
    with open(output_path, "wb") as f:
        f.write(data)

    key_char = chr(skip_key) if 65 <= skip_key <= 90 else str(skip_key)
    print(f"\nSUCCESS: Applied Undertale mod patches to '{output_path}'!")
    print(f"  - Cutscene Skip Key: '{key_char}' (KeyCode: {skip_key})")
    print(
        f"  - Death Gambling: {'Enabled' if enable_gambling else 'Disabled'} "
        f"(Lose item penalty: {'Yes' if item_penalty else 'No'})"
    )
    print(
        f"  - Call Mysterious Number: {'Enabled' if enable_mysterious_call else 'Disabled'} "
        f"(Number: {mysterious_number})"
    )
    print("\nTo restore your original unmodded game at any time, run: python patch_data_win.py -r")
    return True


def main():
    """Main CLI entry point for mod patcher."""
    parser = argparse.ArgumentParser(
        description="Standalone Undertale Mod Patcher (Steam & Xbox PC)"
    )
    parser.add_argument("data_win", nargs="?", help="Path to Undertale game file")
    parser.add_argument("--key", "-k", type=int, help="Skip keycode (e.g. 83 for 'S')")
    parser.add_argument("--gambling", type=int, choices=[0, 1], help="Enable (1) / disable (0)")
    parser.add_argument("--item-penalty", type=int, choices=[0, 1], help="Item loss penalty")
    parser.add_argument("--mysterious-call", type=int, choices=[0, 1], help="Call mysterious num")
    parser.add_argument("--number", type=int, help="Set mysterious phone number")
    parser.add_argument("--restore", "-r", action="store_true", help="Restore original game")
    parser.add_argument("--ini", default="skip_key.ini", help="Path to skip_key.ini file")

    args = parser.parse_args()

    if args.restore:
        success = restore_original_game(args.data_win)
        if not success:
            sys.exit(1)
        return

    config = load_mod_config(args.ini)
    if args.key is not None:
        config['skip_key'] = args.key
    if args.gambling is not None:
        config['enable_gambling'] = args.gambling
    if args.item_penalty is not None:
        config['item_penalty'] = args.item_penalty
    if args.mysterious_call is not None:
        config['enable_mysterious_call'] = args.mysterious_call
    if args.number is not None:
        config['mysterious_number'] = args.number

    success = patch_data_win(args.data_win, config=config)
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
