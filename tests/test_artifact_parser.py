import unittest
from monitor.artifact_parser import parse_artifacts

class TestArtifactParser(unittest.TestCase):
    def test_parse_artifacts(self):
        text = '[FILE:CREATE:foo.py] some text [FILE:UPDATE:bar.md]'
        artifacts = parse_artifacts(text)
        self.assertEqual(len(artifacts), 2)
        self.assertEqual(artifacts[0]['operation'], 'CREATE')
        self.assertEqual(artifacts[0]['filename'], 'foo.py')
        self.assertEqual(artifacts[1]['operation'], 'UPDATE')
        self.assertEqual(artifacts[1]['filename'], 'bar.md')

if __name__ == '__main__':
    unittest.main()
