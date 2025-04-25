import unittest
import os
import json
from unittest.mock import patch
from config_manager import ProjectConfig, save_configs, load_configs, save_psync_file, encrypt_data, decrypt_data, CONFIG_PATH

class TestConfigManager(unittest.TestCase):
    def setUp(self):
        self.test_configs = {
            'space1': ProjectConfig('space1', 'C:/Projects/AI', '2025-04-25', {'a.py': 'A', 'b.py': 'B'})
        }
        # Záloha původního configu
        if os.path.exists(CONFIG_PATH):
            os.rename(CONFIG_PATH, CONFIG_PATH + '.bak')

    def tearDown(self):
        if os.path.exists(CONFIG_PATH):
            os.remove(CONFIG_PATH)
        if os.path.exists(CONFIG_PATH + '.bak'):
            os.rename(CONFIG_PATH + '.bak', CONFIG_PATH)

    def test_encrypt_decrypt(self):
        text = 'secret_path'
        encrypted = encrypt_data(text.encode('utf-8'))
        decrypted = decrypt_data(encrypted).decode('utf-8')
        self.assertEqual(text, decrypted)

    def test_save_and_load_configs(self):
        save_configs(self.test_configs)
        loaded = load_configs()
        self.assertEqual(loaded['space1'].spaceId, 'space1')
        self.assertEqual(loaded['space1'].localPath, 'C:/Projects/AI')
        self.assertEqual(loaded['space1'].fileMappings['a.py'], 'A')

    def test_save_psync_file(self):
        path = 'test.psync'
        save_psync_file('proj-x', 'D:/Projects/AI', 'ak_123', ['.py', '.md'], path)
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.assertEqual(data['spaceId'], 'proj-x')
        self.assertEqual(data['localRoot'], 'D:/Projects/AI')
        self.assertEqual(data['encryptionKey'], 'ak_123')
        self.assertIn('.py', data['fileTypes'])
        os.remove(path)

if __name__ == '__main__':
    unittest.main()
