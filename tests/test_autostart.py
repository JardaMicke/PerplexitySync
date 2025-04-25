import unittest
from unittest.mock import patch, MagicMock
from gui.autostart import enable_autostart, disable_autostart

class TestAutostart(unittest.TestCase):
    @patch('winreg.OpenKey')
    @patch('winreg.SetValueEx')
    @patch('winreg.CloseKey')
    def test_enable_autostart(self, mock_close, mock_set, mock_open):
        enable_autostart(app_name='TestApp', exe_path='C:/Test/test.exe')
        mock_open.assert_called()
        mock_set.assert_called_with(mock_open.return_value, 'TestApp', 0, 1, 'C:/Test/test.exe')
        mock_close.assert_called_with(mock_open.return_value)

    @patch('winreg.OpenKey')
    @patch('winreg.DeleteValue')
    @patch('winreg.CloseKey')
    def test_disable_autostart(self, mock_close, mock_delete, mock_open):
        disable_autostart(app_name='TestApp')
        mock_open.assert_called()
        mock_delete.assert_called_with(mock_open.return_value, 'TestApp')
        mock_close.assert_called_with(mock_open.return_value)

if __name__ == '__main__':
    unittest.main()
