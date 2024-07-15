
class User:

    def __init__(self, sock):
        self.sock = sock
        self.id = id(sock)
        self.name = None
        self.send_q = []
        self.recv_q = []
    
    def get_next_msg(self):
        try:
            return self.send_q.pop(0)
        except:
            return ''