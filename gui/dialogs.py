import ctypes
import tkinter as tk
from tkinter import filedialog

def select_folder_dialog():
    # Použije nativní dialog přes tkinter (SHBrowseForFolder lze doplnit přes ctypes)
    root = tk.Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title='Vyberte složku projektu')
    root.destroy()
    return folder
