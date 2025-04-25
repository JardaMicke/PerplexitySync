import unittest
from unittest.mock import patch
from gui.dialogs import select_folder_dialog

class TestDialogs(unittest.TestCase):
    @patch('tkinter.filedialog.askdirectory', return_value='C:/Projects/Test')
    @patch('tkinter.Tk')
    def test_select_folder_dialog(self, mock_tk, mock_askdirectory):
        folder = select_folder_dialog()
        self.assertEqual(folder, 'C:/Projects/Test')
        mock_tk.return_value.withdraw.assert_called()
        mock_tk.return_value.destroy.assert_called()

if __name__ == '__main__':
    unittest.main()
