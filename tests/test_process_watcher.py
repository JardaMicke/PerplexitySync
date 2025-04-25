import unittest
from unittest.mock import patch
import monitor.process_watcher as pw

class TestProcessWatcher(unittest.TestCase):
    @patch('win32com.client.GetObject')
    def test_detects_perplexity(self, mock_getobject):
        class FakeProcess:
            Name = 'perplexity.exe'
        mock_wmi = type('FakeWMI', (), {'InstancesOf': lambda self, _: [FakeProcess()]})()
        mock_getobject.return_value = mock_wmi
        detected = []
        def cb():
            detected.append(True)
        pw.watch_perplexity_process(cb, poll_interval=0)
        self.assertTrue(detected)

if __name__ == '__main__':
    unittest.main()
