import winreg
import os

def enable_autostart(app_name='PerplexitySync', exe_path=None):
    if exe_path is None:
        exe_path = os.path.abspath(__file__)
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, exe_path)
    winreg.CloseKey(key)

def disable_autostart(app_name='PerplexitySync'):
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
    try:
        winreg.DeleteValue(key, app_name)
    except FileNotFoundError:
        pass
    winreg.CloseKey(key)
