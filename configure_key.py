#!/usr/bin/env python3
"""
Standalone Key & Mod Configuration Utility for SKIPscene Undertale Mod.
Allows easy selection of cutscene skip key, death gambling settings,
and mysterious phone number options. No external dependencies required.
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
    """Load configuration INI file."""
    config = configparser.ConfigParser(inline_comment_prefixes=(';', '#'))
    config.optionxform = str  # Preserve casing of key names
    if ini_path.exists():
        config.read(ini_path)
    if 'Settings' not in config:
        config['Settings'] = {}
    return config


def save_ini(config: configparser.ConfigParser, ini_path: Path):
    """Save configuration INI file."""
    with open(ini_path, 'w', encoding='utf-8') as f:
        config.write(f)


def get_key_code(key_str: str) -> int:
    """Map string key name to numerical keycode."""
    key_str = key_str.strip().upper()
    if key_str.isdigit():
        return int(key_str)
    if key_str in KEY_MAP:
        return KEY_MAP[key_str]
    if len(key_str) == 1 and 'A' <= key_str <= 'Z':
        return ord(key_str)
    raise ValueError(f"Unknown or unsupported key: '{key_str}'")


def update_config_from_args(config, args, ini_filename: str) -> bool:
    """Update settings in config object based on CLI arguments."""
    has_updates = False
    if args.key:
        code = get_key_code(args.key)
        config['Settings']['SkipKey'] = str(code)
        print(f"Updated SkipKey to '{args.key.upper()}' (KeyCode: {code}) in {ini_filename}")
        has_updates = True

    if args.speed is not None:
        config['Settings']['FastForwardSpeed'] = str(args.speed)
        print(f"Updated FastForwardSpeed to {args.speed}")
        has_updates = True

    if args.gambling is not None:
        config['Settings']['EnableGamblingOnDeath'] = str(args.gambling)
        print(f"Updated EnableGamblingOnDeath to {args.gambling}")
        has_updates = True

    if args.item_penalty is not None:
        config['Settings']['GambleItemLossPenalty'] = str(args.item_penalty)
        print(f"Updated GambleItemLossPenalty to {args.item_penalty}")
        has_updates = True

    if args.mysterious_call is not None:
        config['Settings']['EnableCallMysteriousNumber'] = str(args.mysterious_call)
        print(f"Updated EnableCallMysteriousNumber to {args.mysterious_call}")
        has_updates = True

    if args.number is not None:
        config['Settings']['MysteriousNumber'] = str(args.number)
        print(f"Updated MysteriousNumber to {args.number}")
        has_updates = True

    return has_updates


def main():
    """Main CLI entry point for key & mod configuration."""
    parser = argparse.ArgumentParser(
        description="Configure cutscene skip, gambling, and mysterious number settings."
    )
    parser.add_argument('--key', '-k', type=str, help="Key to assign for skipping (e.g. S, A)")
    parser.add_argument('--speed', '-s', type=int, help="Fast forward room speed (default 300)")
    parser.add_argument('--gambling', type=int, choices=[0, 1], help="Enable (1) / disable (0)")
    parser.add_argument('--item-penalty', type=int, choices=[0, 1], help="Item loss penalty")
    parser.add_argument('--mysterious-call', type=int, choices=[0, 1], help="Mysterious call")
    parser.add_argument('--number', type=int, help="Mysterious phone number (e.g. 666)")
    parser.add_argument('--ini', type=str, default="skip_key.ini", help="Path to INI file")

    args = parser.parse_args()
    ini_path = Path(args.ini)
    config = load_ini(ini_path)

    try:
        has_cli_updates = update_config_from_args(config, args, ini_path.name)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    if not has_cli_updates and len(sys.argv) == 1:
        current_code = config['Settings'].get('SkipKey', '83')
        print(f"Current SkipKey Code: {current_code}")
        prompt = "Enter new key (e.g. S, A, Z, Space, Shift) or keycode (Enter to skip): "
        user_input = input(prompt).strip()
        if user_input:
            try:
                code = get_key_code(user_input)
                config['Settings']['SkipKey'] = str(code)
                print(f"Updated SkipKey to '{user_input.upper()}' (KeyCode: {code})")
            except ValueError as e:
                print(f"Error: {e}")
                sys.exit(1)

    save_ini(config, ini_path)


if __name__ == '__main__':
    main()
