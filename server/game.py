
class Game:

    def __init__(self, server):

        self.potential_readers = [server]
        self.potential_writers = []
        self.potential_errors = []
        self.timeout = 1
        self.num_players = 0
