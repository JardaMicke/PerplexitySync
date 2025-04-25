import unittest
from fastapi.testclient import TestClient
from mcp_server.server import app
import os

class TestMCPServer(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.test_dir = 'C:/Projects/test_mcp'
        self.test_file = os.path.join(self.test_dir, 'foo.txt')
        os.makedirs(self.test_dir, exist_ok=True)
        with open(self.test_file, 'w') as f:
            f.write('test content')

    def tearDown(self):
        try:
            os.remove(self.test_file)
            os.rmdir(self.test_dir)
        except Exception:
            pass

    def test_get_file(self):
        response = self.client.get('/file', params={'path': self.test_file})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'test content')

    def test_list_dir(self):
        response = self.client.get('/list', params={'dir': self.test_dir})
        self.assertEqual(response.status_code, 200)
        self.assertIn('foo.txt', response.json().get('files', []))

    def test_get_file_denied(self):
        response = self.client.get('/file', params={'path': 'C:/Windows/system32/cmd.exe'})
        self.assertEqual(response.status_code, 403)

if __name__ == '__main__':
    unittest.main()
