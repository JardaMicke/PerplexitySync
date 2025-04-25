import unittest
from unittest.mock import patch, MagicMock
from ollama_integration.ollama_client import generate_code

class TestOllamaClient(unittest.TestCase):
    @patch('requests.post')
    def test_generate_code_stream(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.__enter__.return_value = mock_resp
        mock_resp.iter_lines.return_value = [b'{"response": "foo"}', b'{"response": "bar"}']
        mock_resp.raise_for_status = lambda: None
        mock_post.return_value = mock_resp
        result = list(generate_code('test prompt', stream=True))
        self.assertIn('{"response": "foo"}', result)
        self.assertIn('{"response": "bar"}', result)

    @patch('requests.post')
    def test_generate_code_nonstream(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.__enter__.return_value = mock_resp
        mock_resp.json.return_value = {'response': 'baz'}
        mock_resp.raise_for_status = lambda: None
        mock_post.return_value = mock_resp
        result = list(generate_code('test prompt', stream=False))
        self.assertIn('baz', result[0])

if __name__ == '__main__':
    unittest.main()
