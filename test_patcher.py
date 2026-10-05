#!/usr/bin/env python3
"""
Unit tests for Undertale mod patcher and configuration tools.
"""

import os
import shutil
import struct
import unittest
import tempfile

from patch_data_win import (
    patch_data_win, restore_original_game, load_mod_config, GameMakerDataWin
)


class TestUndertalePatcher(unittest.TestCase):
    """Test suite for Undertale binary patcher and configuration loading."""

    def setUp(self):
        """Set up temporary test workspace."""
        self.temp_dir = tempfile.mkdtemp()
        self.data_win_path = os.path.join(self.temp_dir, "data.win")
        self.ini_path = os.path.join(self.temp_dir, "skip_key.ini")
        self._create_dummy_data_win(self.data_win_path)

    def tearDown(self):
        """Tear down temporary test workspace."""
        shutil.rmtree(self.temp_dir)

    def _create_dummy_data_win(self, filepath):
        """Helper to create dummy GameMaker FORM container."""
        gen8_body = bytearray(200)
        gen8_size = len(gen8_body)

        chunk_header = b'GEN8' + struct.pack('<I', gen8_size)
        form_body = chunk_header + gen8_body
        form_size = len(form_body)

        file_bytes = b'FORM' + struct.pack('<I', form_size) + form_body
        with open(filepath, 'wb') as f:
            f.write(file_bytes)

    def test_gamemaker_parsing(self):
        """Test GameMaker chunk header parsing."""
        with open(self.data_win_path, 'rb') as f:
            data = bytearray(f.read())
        gw = GameMakerDataWin(data)
        self.assertIn('GEN8', gw.chunks)

    def test_patch_and_restore(self):
        """Test binary patching tags injection, updating, and backup restoration."""
        config = {
            'skip_key': 65,  # Key 'A'
            'enable_gambling': 1,
            'item_penalty': 1,
            'enable_mysterious_call': 1,
            'mysterious_number': 777,
        }

        # Apply patch
        success = patch_data_win(self.data_win_path, config=config)
        self.assertTrue(success)

        # Check backup file exists
        backup_path = self.data_win_path + ".bak"
        self.assertTrue(os.path.exists(backup_path))

        # Verify patch tags injected into patched file
        with open(self.data_win_path, 'rb') as f:
            patched_data = f.read()

        self.assertIn(b'SKIP_KEY_CFG', patched_data)
        self.assertIn(b'GAMBLE_DEATH_CFG', patched_data)
        self.assertIn(b'MYST_NUMBER_CFG', patched_data)

        # Re-patching existing tags
        config['skip_key'] = 90  # Key 'Z'
        config['mysterious_number'] = 999
        success_repatch = patch_data_win(self.data_win_path, config=config)
        self.assertTrue(success_repatch)

        # Restore original file
        restore_success = restore_original_game(self.data_win_path)
        self.assertTrue(restore_success)

        # Verify original data restored (tags should be absent from clean original)
        with open(self.data_win_path, 'rb') as f:
            restored_data = f.read()
        self.assertNotIn(b'SKIP_KEY_CFG', restored_data)

    def test_ini_config_loading(self):
        """Test configuration loading from INI file."""
        ini_content = (
            "[Settings]\n"
            "SkipKey = 70\n"
            "EnableGamblingOnDeath = 1\n"
            "GambleItemLossPenalty = 0\n"
            "EnableCallMysteriousNumber = 1\n"
            "MysteriousNumber = 42\n"
        )
        with open(self.ini_path, 'w', encoding='utf-8') as f:
            f.write(ini_content)

        cfg = load_mod_config(self.ini_path)
        self.assertEqual(cfg['skip_key'], 70)
        self.assertEqual(cfg['enable_gambling'], 1)
        self.assertEqual(cfg['item_penalty'], 0)
        self.assertEqual(cfg['enable_mysterious_call'], 1)
        self.assertEqual(cfg['mysterious_number'], 42)


if __name__ == '__main__':
    unittest.main()
