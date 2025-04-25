import psutil
import time
import win32com.client

def watch_perplexity_process(on_detect, poll_interval=2):
    """
    Sleduje běžící proces 'perplexity.exe' pomocí WMI. Pokud je detekován, zavolá callback.
    """
    wmi = win32com.client.GetObject('winmgmts:')
    while True:
        processes = wmi.InstancesOf('Win32_Process')
        for process in processes:
            if process.Name.lower() == 'perplexity.exe':
                on_detect()
                return
        time.sleep(poll_interval)
