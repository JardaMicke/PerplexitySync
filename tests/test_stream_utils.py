import unittest
from ollama_integration.stream_utils import extract_text_from_stream_line
import json

class TestStreamUtils(unittest.TestCase):
    def test_extract_text(self):
        line = json.dumps({'response': 'Hello world!'})
        self.assertEqual(extract_text_from_stream_line(line), 'Hello world!')
    def test_extract_text_empty(self):
        self.assertEqual(extract_text_from_stream_line('{}'), '')
    def test_extract_text_invalid(self):
        self.assertEqual(extract_text_from_stream_line('not json'), '')

if __name__ == '__main__':
    unittest.main()
