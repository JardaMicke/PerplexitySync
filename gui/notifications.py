from win10toast import ToastNotifier

def notify(message, title="PerplexitySync"):
    toaster = ToastNotifier()
    toaster.show_toast(title, message, duration=5, threaded=True)
