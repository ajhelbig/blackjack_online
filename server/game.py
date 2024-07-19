from games.blackjack.player import Player

class Game:

    def __init__(self, name):
        self.name = name
        self.players = []
        self.num_players = 0

    def add_player(self, username, bank):
        new_player = Player(username, bank)
        self.players.append(new_player)
        self.num_players += 1
        print(f"num players: {self.num_players}")

    def load_blackjack_game(self, level, house_bank):
        pass
