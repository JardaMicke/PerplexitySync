import unittest
from mcp_server.exec import exec_cmd_as_admin

class TestExec(unittest.TestCase):
    def test_safe_command(self):
        result = exec_cmd_as_admin('echo Hello')
        self.assertIn('stdout', result)
        self.assertIn('Hello', result['stdout'])
        self.assertEqual(result['returncode'], 0)

    def test_unsafe_command(self):
        result = exec_cmd_as_admin('del C:/Windows/System32')
        self.assertIn('error', result)
        self.assertEqual(result['error'], 'Command not allowed')

    def test_python_command(self):
        result = exec_cmd_as_admin('python --version')
        self.assertIn('stdout', result)
        self.assertEqual(result['returncode'], 0)

if __name__ == '__main__':
    unittest.main()
