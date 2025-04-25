import unittest
from mcp_server.security import is_allowed_path, validate_path

class TestSecurity(unittest.TestCase):
    def test_is_allowed_path(self):
        allowed = [r'C:/Projects', r'D:/Workspace']
        self.assertTrue(is_allowed_path(r'C:/Projects/foo.txt', allowed))
        self.assertFalse(is_allowed_path(r'C:/Other/bar.txt', allowed))

    def test_validate_path(self):
        self.assertTrue(validate_path(r'C:/Projects/foo.txt'))
        self.assertFalse(validate_path(r'../../etc/passwd'))
        # Kombinovaný test: traversal projde validate_path, ale neprojde is_allowed_path
        allowed = [r'C:/Projects']
        path = r'C:/Projects/../Windows/system32'
        self.assertTrue(validate_path(path))
        self.assertFalse(is_allowed_path(path, allowed))

if __name__ == '__main__':
    unittest.main()
