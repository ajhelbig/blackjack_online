import socket

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

        totalsent = 0

        while totalsent < len(msg):

            sent = self.s.send(msg[totalsent:].encode())

            if sent == 0:
                raise RuntimeError("socket connection broken")

            totalsent = totalsent + sent

    def recv_msg(self): #receives null byte delimited messages

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

        return (b''.join(chunks)).decode()

    def close_connection(self):
        self.s.close()
