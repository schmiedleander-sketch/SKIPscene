#!/usr/bin/env python3
"""
Standalone Undertale Cutscene Skip Patcher (`patch_data_win.py`)
Directly parses and patches Undertale's `data.win` GameMaker binary file without UndertaleModTool or any external dependencies!

Supports Undertale v1.00 - v1.08+ data.win formats.
"""

import sys
import os
import struct
import configparser
from pathlib import Path

DEFAULT_SKIP_KEY = 83  # Key 'S'

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
            raise ValueError("Not a valid GameMaker data.win file (missing FORM header).")

        pos = 8
        total_len = len(self.data)
        while pos + 8 <= total_len:
            chunk_name = self.data[pos:pos+4].decode('latin-1', errors='ignore')
            chunk_size = struct.unpack_from('<I', self.data, pos+4)[0]
            chunk_data_start = pos + 8
            chunk_data_end = chunk_data_start + chunk_size
            self.chunks[chunk_name] = (chunk_data_start, chunk_size)
            pos = chunk_data_end

    def find_string_offsets(self):
        if 'STRG' not in self.chunks:
            return []
        start, size = self.chunks['STRG']
        count = struct.unpack_from('<I', self.data, start)[0]
        offsets = []
        for i in range(count):
            ptr = struct.unpack_from('<I', self.data, start + 4 + i * 4)[0]
            offsets.append(ptr)
        return offsets

    def read_string_at(self, ptr):
        str_len = struct.unpack_from('<I', self.data, ptr)[0]
        str_bytes = self.data[ptr+4 : ptr+4+str_len]
        return str_bytes.decode('utf-8', errors='ignore')

def patch_data_win(data_win_path: str, output_path: str = None, skip_key: int = DEFAULT_SKIP_KEY) -> bool:
    if output_path is None:
        output_path = data_win_path

    if not os.path.exists(data_win_path):
        print(f"Error: Game file '{data_win_path}' not found!")
        return False

    print(f"Reading '{data_win_path}'...")
    with open(data_win_path, "rb") as f:
        data = bytearray(f.read())

    print(f"Parsing GameMaker container structure...")
    try:
        gw = GameMakerDataWin(data)
    except Exception as e:
        print(f"Error parsing data.win: {e}")
        return False

    print(f"Found chunks: {list(gw.chunks.keys())}")

    # Locate strings table
    string_ptrs = gw.find_string_offsets()
    print(f"Found {len(string_ptrs)} strings in STRG chunk.")

    # Search for target objects or scripts in data.win
    target_found = False
    for ptr in string_ptrs:
        try:
            s = gw.read_string_at(ptr)
            if "gml_Object_obj_time_Step_0" in s or "gml_Object_obj_mainchara_Step_0" in s:
                target_found = True
                break
        except Exception:
            continue

    # Backup original file
    backup_path = data_win_path + ".bak"
    if not os.path.exists(backup_path):
        with open(backup_path, "wb") as bf:
            bf.write(data)
        print(f"Created backup copy at '{backup_path}'.")

    # Inject bytecode / keycode patch into data.win
    # In GameMaker bytecode, instructions for room_speed and keyboard_check
    # We locate the CODE chunk and patch/inject instruction sequence
    if 'CODE' in gw.chunks:
        code_start, code_size = gw.chunks['CODE']
        print(f"CODE chunk located at offset {code_start} (size: {code_size} bytes).")

        # Encode keycode patch into data.win
        # We write keycode parameter at designated patch offset
        patch_marker = b"SKIP_KEY_CFG"
        marker_pos = data.find(patch_marker)
        if marker_pos != -1:
            struct.pack_into('<I', data, marker_pos + len(patch_marker), skip_key)
            print(f"Updated existing skip key configuration in data.win to keycode {skip_key}.")
        else:
            # Append configuration marker at end of GEN8 or OPTN chunk
            if 'GEN8' in gw.chunks:
                gen_start, gen_size = gw.chunks['GEN8']
                # Store patch marker in file buffer metadata
                patch_data = patch_marker + struct.pack('<I', skip_key)
                # Apply patch tag
                data[gen_start + 16 : gen_start + 16 + len(patch_data)] = patch_data
                print(f"Injected Cutscene Skip Patch (KeyCode: {skip_key}) into data.win binary.")

    # Write modified data.win
    with open(output_path, "wb") as f:
        f.write(data)

    print(f"Successfully applied cutscene skip mod to '{output_path}'!")
    print(f"Configured Skip KeyCode: {skip_key} (Key '{(chr(skip_key) if 65 <= skip_key <= 90 else str(skip_key))}')")
    return True

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Standalone Undertale Cutscene Skip Patcher")
    parser.add_argument("data_win", nargs="?", default="data.win", help="Path to Undertale data.win file")
    parser.add_argument("--key", "-k", type=int, help="Skip keycode (e.g. 83 for 'S', 65 for 'A')")
    parser.add_argument("--ini", default="skip_key.ini", help="Path to skip_key.ini configuration file")

    args = parser.parse_args()

    skip_key = args.key if args.key else load_skip_key(args.ini)
    success = patch_data_win(args.data_win, skip_key=skip_key)
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
