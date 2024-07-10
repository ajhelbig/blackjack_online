
class Game:

    def __init__(self, server):

        self.game_id = id(self)
        self.potential_readers = []
        self.potential_writers = []
        self.potential_errors = []
        self.timeout = 1
        self.num_players = 0
