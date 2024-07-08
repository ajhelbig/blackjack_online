import socket
import threading

chunk_size = 4096

class Client:

    def __init__(self, s=None):
        if s == None:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.s = s

    def connect(self, host, port):
        self.s.connect((host, port))

    def send_msg(self, msg):

        msg = msg + '\0'

        totalsent = 0

        while totalsent < len(msg):

            sent = self.s.send(msg[totalsent:].encode())

            if sent == 0:
                raise RuntimeError("socket connection broken")

            totalsent = totalsent + sent

    def recv_msg(self):

        chunks = []
        bytes_recd = 0

        while True:

            chunk = self.s.recv(chunk_size)

            if chunk == b'':
                raise RuntimeError("socket connection broken")

            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)

            if chunk[-1] == 0:
                break

        msg = b''.join(chunks)

        final_msg = msg[:-1]

        return final_msg.decode()

    def close_connection(self):
        self.s.close()

    def thread_send(self):
        while True:
            msg = input("> ")
            self.send_msg(msg)

    def thread_recv(self):
        while True:
            msg = self.recv_msg()
            print(f"msg recv: {msg}")

    def start(self):
        threading.Thread(target=self.thread_recv).start()
        threading.Thread(target=self.thread_send).start()
