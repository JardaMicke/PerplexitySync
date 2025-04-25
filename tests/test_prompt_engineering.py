import unittest
from ollama_integration.prompt_engineering import build_prompt

class TestPromptEngineering(unittest.TestCase):
    def test_build_prompt(self):
        prompt = build_prompt('python', 'Napiš funkci na součet', 'Projekt X', 'PEP8')
        self.assertIn('[INST]', prompt)
        self.assertIn('python', prompt)
        self.assertIn('Napiš funkci na součet', prompt)
        self.assertIn('Projekt X', prompt)
        self.assertIn('PEP8', prompt)
        self.assertTrue(prompt.strip().endswith('[/INST]'))

if __name__ == '__main__':
    unittest.main()
