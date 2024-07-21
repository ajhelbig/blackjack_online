
class User:

    def __init__(self, sock):
        self.sock = sock
        self.id = id(sock)

        self.name = None
        self.game = None
        self.in_game = False
        self.bank = 0

        self.send_q = []
        self.recv_q = []

    def add_game(self, game):
        self.game = game
        self.in_game = True

    def remove_game(self):
        self.game = None
        self.in_game = False
    
    def get_next_msg(self):
        try:
            return self.send_q.pop(0)
        except:
            return None