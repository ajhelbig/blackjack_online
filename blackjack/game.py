from blackjack.player import Blackjack_Player
from blackjack.deck import Deck

class Game:

    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.players = {}
        self.bets_placed = 0
        self.num_players = 0
        self.max_num_players = 7
        self.house_bank = 1000
        self.player_starting_bank = 0
        self.state = "BET"

        self.deck = Deck(num_decks=1)

    def good_password(self, password):
        return self.password == password

    def add_player(self, username):
        if self.num_players + 1 > self.max_num_players:
            return False
        
        new_player = Blackjack_Player(username, self.player_starting_bank)
        self.players[username] = new_player
        self.num_players += 1
        print(f"Players in game: {self.num_players}")

        return True

    def remove_player(self, username):
        del self.players[username]
        self.num_players -= 1
        print(f"Players in game: {self.num_players}")

    def place_bet(self, username, bet):
        player = self.players[username]

        if player.bet is not None:
            return "BET_ALREADY_PLACED"
        
        player.place_bet(bet)
        self.bets_placed += 1

        if self.bets_placed == self.num_players:
            self.state = "PLAY"

        return "SUCCESS"
    
    def deal(self):
        for player in self.players.values():
            player.get_new_hand(self.deck)

        return "SUCCESS"

    def hit(self, username):
        player = self.players[username]
        player.hit(self.deck)

        if player.busted:
            return "BUSTED"
        
        return "SUCCESS"

    def stand(self, username):
        player = self.players[username]
        player.stand()
        return "SUCCESS"

    def double_down(self, username):
        player = self.players[username]
        player.double_down(self.deck)

        if player.busted:
            return "BUSTED"

        return "SUCCESS"
