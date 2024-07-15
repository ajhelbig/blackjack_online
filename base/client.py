import socket
import threading

class Client:

    def __init__(self, s=None):
        if s == None:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.s = s

        self.chunk_size = 4096
        self.send_q = []
        self.recv_q = []

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

            chunk = self.s.recv(self.chunk_size)

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

    def thread_send(self, send_q):
        while True:
            try:
                msg = send_q.pop(0)
                if msg:
                    self.send_msg(msg)
            except:
                pass

    def thread_recv(self, recv_q):
        while True:
            msg = self.recv_msg()
            recv_q.append(msg)

    def await_msg(self, msg_sent):
        split_msg = msg_sent.split()
        num_resp = int(split_msg[1])
        responses = split_msg[2:2+num_resp]

        while True:
            try:
                resp = self.recv_q.pop(0)
                if resp in responses:
                    return resp
                else:
                    self.recv_q.append(resp)
            except:
                pass

    def start(self):
        threading.Thread(target=self.thread_recv, args=(self.recv_q,)).start()
        threading.Thread(target=self.thread_send, args=(self.send_q,)).start()