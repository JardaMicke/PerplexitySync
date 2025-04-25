import unittest
from unittest.mock import patch
from gui.notifications import notify

class TestNotifications(unittest.TestCase):
    @patch('win10toast.ToastNotifier.show_toast')
    @patch('win10toast.ToastNotifier.__init__', return_value=None)
    def test_notify(self, mock_init, mock_show):
        notify('Test zpráva', title='TestTitulek')
        mock_show.assert_called_with('TestTitulek', 'Test zpráva', duration=5, threaded=True)

if __name__ == '__main__':
    unittest.main()
