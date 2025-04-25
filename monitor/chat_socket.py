import socket

def start_chat_listener(on_message, host='localhost', port=9000):
    """
    Otevře TCP socket a předává přijaté zprávy do on_message(text)
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            text = data.decode('utf-8')
            on_message(text)
