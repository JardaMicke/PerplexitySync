import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import threading
from gui.dialogs import select_folder_dialog
from gui.notifications import notify
from gui.autostart import enable_autostart, disable_autostart


def create_image():
    # Jednoduchá ikona
    image = Image.new('RGB', (64, 64), color='white')
    d = ImageDraw.Draw(image)
    d.rectangle([16, 16, 48, 48], fill='blue')
    d.text((22, 26), 'P', fill='white')
    return image


def on_select_folder(icon, item):
    folder = select_folder_dialog()
    if folder:
        notify(f'Vybrán projektový adresář: {folder}')


def on_exit(icon, item):
    icon.stop()


def run_tray():
    menu = (
        item('Vybrat složku', on_select_folder),
        item('Povolit autostart', lambda icon, item: enable_autostart()),
        item('Zakázat autostart', lambda icon, item: disable_autostart()),
        item('Ukončit', on_exit)
    )
    icon = pystray.Icon('PerplexitySync', create_image(), 'PerplexitySync', menu)
    icon.run()

if __name__ == '__main__':
    threading.Thread(target=run_tray, daemon=True).start()
