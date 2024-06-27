import socket

MSGLEN = 41
chunk_size = 1024

class ClientSocket:

    def __init__(self, s=None):
        if s == None:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.s = s

        print("client socket created")

    def connect(self, host, port):
        self.s.connect((host, port))
        print(f"client connectd to {host}, {port}")

    def c_send(self, msg):
        totalsent = 0
        while totalsent < MSGLEN:
            sent = self.s.send(msg[totalsent:].encode())
            if sent == 0:
                raise RuntimeError("socket connection broken")

            totalsent = totalsent + sent

    def c_recv(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.s.recv(min(MSGLEN - bytes_recd, chunk_size))
            # print("[" + chunk.decode() + "]")
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)

        return (b''.join(chunks)).decode()

    def c_close(self):
        self.s.close()

client = ClientSocket()

client.connect('127.0.0.1', 5890)

print(client.c_recv())

client.c_close()
