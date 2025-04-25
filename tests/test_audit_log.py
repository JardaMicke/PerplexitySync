import unittest
import os
import json
from mcp_server.audit_log import AuditLogger

class TestAuditLogger(unittest.TestCase):
    def setUp(self):
        self.log_path = 'test_audit.log'
        self.key = b'testkey'
        if os.path.exists(self.log_path):
            os.remove(self.log_path)
        self.logger = AuditLogger(self.log_path, self.key)

    def tearDown(self):
        if os.path.exists(self.log_path):
            os.remove(self.log_path)

    def test_log_entry(self):
        self.logger.log('READ', 'C:/Projects/foo.txt', user='tester')
        with open(self.log_path, 'r', encoding='utf-8') as f:
            entry = json.loads(f.readline())
        self.assertEqual(entry['operation'], 'READ')
        self.assertEqual(entry['path'], 'C:/Projects/foo.txt')
        self.assertEqual(entry['user'], 'tester')
        self.assertIn('hmac', entry)

if __name__ == '__main__':
    unittest.main()
