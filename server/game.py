from games.blackjack.player import Player

class Game:

    def __init__(self, name, level=None, house_bank=None):
        self.name = name
        self.players = {}
        self.num_players = 0
        self.level = 1
        self.house_bank = 1000

        if house_bank is not None:
            self.house_bank = house_bank

        if level is not None:
            self.level = level

    def add_player(self, username, bank):
        new_player = Player(username, bank)
        self.players[username] = new_player
        self.num_players += 1
        print(f"num players: {self.num_players}")

    def remove_player(self, username):
        del self.player[username]
        self.num_players -= 1

    def load_blackjack_game(self, level, house_bank):
        self.level = level
        self.house_bank = house_bank
        print(f"load level: {level}")
        print(f"load house bank: {house_bank}")
