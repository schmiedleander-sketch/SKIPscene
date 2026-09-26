#!/usr/bin/env python3
"""
Standalone Key Configuration Utility for SKIPscene Undertale Mod.
Allows easy selection and swapping of the cutscene skip key.
No external dependencies required (uses built-in standard Python modules).
"""

import sys
import argparse
import configparser
from pathlib import Path

# Common key codes for Undertale / GameMaker
KEY_MAP = {
    'A': 65, 'B': 66, 'C': 67, 'D': 68, 'E': 69, 'F': 70,
    'G': 71, 'H': 72, 'I': 73, 'J': 74, 'K': 75, 'L': 76,
    'M': 77, 'N': 78, 'O': 79, 'P': 80, 'Q': 81, 'R': 82,
    'S': 83, 'T': 84, 'U': 85, 'V': 86, 'W': 87, 'X': 88,
    'Y': 89, 'Z': 90,
    '0': 48, '1': 49, '2': 50, '3': 51, '4': 52,
    '5': 53, '6': 54, '7': 55, '8': 56, '9': 57,
    'SPACE': 32, 'SHIFT': 16, 'CTRL': 17, 'ALT': 18, 'TAB': 9, 'ENTER': 13
}

def load_ini(ini_path: Path) -> configparser.ConfigParser:
    config = configparser.ConfigParser(inline_comment_prefixes=(';', '#'))
    config.optionxform = str  # Preserve casing of key names
    if ini_path.exists():
        config.read(ini_path)
    if 'Settings' not in config:
        config['Settings'] = {}
    return config

def save_ini(config: configparser.ConfigParser, ini_path: Path):
    with open(ini_path, 'w') as f:
        config.write(f)

def get_key_code(key_str: str) -> int:
    key_str = key_str.strip().upper()
    if key_str.isdigit():
        return int(key_str)
    if key_str in KEY_MAP:
        return KEY_MAP[key_str]
    if len(key_str) == 1 and 'A' <= key_str <= 'Z':
        return ord(key_str)
    raise ValueError(f"Unknown or unsupported key: '{key_str}'")

def main():
    parser = argparse.ArgumentParser(description="Configure cutscene skip key for Undertale.")
    parser.add_argument('--key', '-k', type=str, help="Key to assign for skipping (e.g. S, A, Z, X, Space, Shift, 83)")
    parser.add_argument('--speed', '-s', type=int, help="Fast forward room speed (default 300)")
    parser.add_argument('--ini', type=str, default="skip_key.ini", help="Path to skip_key.ini file")

    args = parser.parse_args()
    ini_path = Path(args.ini)
    config = load_ini(ini_path)

    if args.key:
        try:
            code = get_key_code(args.key)
            config['Settings']['SkipKey'] = str(code)
            print(f"Updated SkipKey to '{args.key.upper()}' (KeyCode: {code}) in {ini_path.name}")
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        current_code = config['Settings'].get('SkipKey', '83')
        print(f"Current SkipKey Code: {current_code}")
        user_input = input("Enter new key (e.g. S, A, Z, X, Space, Shift) or keycode: ").strip()
        if user_input:
            try:
                code = get_key_code(user_input)
                config['Settings']['SkipKey'] = str(code)
                print(f"Updated SkipKey to '{user_input.upper()}' (KeyCode: {code}) in {ini_path.name}")
            except ValueError as e:
                print(f"Error: {e}")
                sys.exit(1)

    if args.speed:
        config['Settings']['FastForwardSpeed'] = str(args.speed)
        print(f"Updated FastForwardSpeed to {args.speed}")

    save_ini(config, ini_path)

if __name__ == '__main__':
    main()
