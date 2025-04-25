import unittest
import os
from context_injector import get_codebase_snapshot, codebase_hash, get_or_cache_codebase, inject_codebase_to_query

class TestContextInjector(unittest.TestCase):
    def setUp(self):
        self.test_dir = 'test_codebase'
        os.makedirs(self.test_dir, exist_ok=True)
        with open(os.path.join(self.test_dir, 'a.py'), 'w') as f:
            f.write('print("A")')
        with open(os.path.join(self.test_dir, 'b.md'), 'w') as f:
            f.write('# Markdown')

    def tearDown(self):
        for fname in ['a.py', 'b.md']:
            try:
                os.remove(os.path.join(self.test_dir, fname))
            except Exception:
                pass
        try:
            os.rmdir(self.test_dir)
        except Exception:
            pass
        cache = os.path.join(os.environ.get('APPDATA', ''), 'PerplexitySync', 'codebase_cache.json')
        if os.path.exists(cache):
            os.remove(cache)

    def test_snapshot_and_hash(self):
        snap = get_codebase_snapshot(self.test_dir, ['.py', '.md'])
        self.assertIn('a.py', snap)
        self.assertIn('b.md', snap)
        h = codebase_hash(snap)
        self.assertIsInstance(h, str)

    def test_cache(self):
        codebase = get_or_cache_codebase(self.test_dir, ['.py', '.md'])
        self.assertIn('a.py', codebase)
        # Druhé volání použije cache
        codebase2 = get_or_cache_codebase(self.test_dir, ['.py', '.md'])
        self.assertEqual(codebase, codebase2)

    def test_inject(self):
        query = 'Jak funguje tento projekt?'
        result = inject_codebase_to_query(query, self.test_dir, ['.py', '.md'])
        self.assertIn('CODEBASE CONTEXT', result)
        self.assertIn('a.py', result)
        self.assertIn('b.md', result)

if __name__ == '__main__':
    unittest.main()
