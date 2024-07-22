from games.blackjack.player import Player

class Game:

    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.players = {}
        self.num_players = 0
        self.max_num_players = 7
        self.house_bank = 1000
        self.player_starting_bank = 0

    def bad_password(self, password):
        if self.password == "NULL":
            return False
        else:
            return self.password == password

    def add_player(self, username):
        if self.num_players + 1 > self.max_num_players:
            return False
        
        new_player = Player(username, self.player_starting_bank)
        self.players[username] = new_player
        self.num_players += 1
        print(f"Players in game: {self.num_players}")

        return True

    def remove_player(self, username):
        del self.players[username]
        self.num_players -= 1
        print(f"Players in game: {self.num_players}")
