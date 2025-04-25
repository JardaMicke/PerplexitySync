import unittest
import socket
import threading
from monitor.chat_socket import start_chat_listener

class TestChatSocket(unittest.TestCase):
    def test_message_received(self):
        messages = []
        def on_message(msg):
            messages.append(msg)
        # Start listener in a thread
        listener_thread = threading.Thread(target=start_chat_listener, args=(on_message, 'localhost', 9001), daemon=True)
        listener_thread.start()
        # Client sends message
        with socket.create_connection(('localhost', 9001)) as s:
            s.sendall(b'Hello!')
        listener_thread.join(timeout=0.2)
        self.assertIn('Hello!', messages)

if __name__ == '__main__':
    unittest.main()
