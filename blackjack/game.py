from blackjack.player import Blackjack_Player
from blackjack.deck import Deck

class Game:

    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.players = {}
        self.dealer = Blackjack_Player("Dealer", 1000)
        self.bets_placed = 0
        self.num_players = 0
        self.player_turn = 0
        self.max_num_players = 5
        self.player_starting_bank = 500
        self.state = "BET"

        self.deck = Deck(num_decks=1)

    def next_player_turn(self):
        self.player_turn += 1
        self.player_turn %= self.num_players

        if self.player_turn == 0:
            return None

        return self.player_turn
    
    def get_player_turn(self):
        return self.players[list(self.players.keys())[self.player_turn]].name
    
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
            self.deal()

        return "SUCCESS"
    
    def get_data(self):
        game_data = []

        game_data.append(self.dealer.get_data())

        for player in self.players.values():
            game_data.append(player.get_data())

        return game_data
    
    def deal(self):
        for player in self.players.values():
            player.get_new_hand(self.deck)

        self.dealer.get_new_hand(self.deck)

    def players_turn(self, username):
        return list(self.players.keys())[self.player_turn] == username

    def hit(self, username):
        if self.players_turn(username):
            player = self.players[username]
            player.hit(self.deck)

            if player.busted:
                if self.next_player_turn() is None:
                    self.state = "DEALER_PLAY"
                return "BUSTED"
            
            return "SUCCESS"
        else:
            return "NOT_PLAYERS_TURN"

    def stand(self, username):
        if self.players_turn(username):
            player = self.players[username]
            player.stand()

            if self.next_player_turn() is None:
                self.state = "DEALER_PLAY"
            
            return "SUCCESS"
        else:
            return "NOT_PLAYERS_TURN"

    def double_down(self, username):
        if self.players_turn(username):
            player = self.players[username]
            player.double_down(self.deck)

            if self.next_player_turn() is None:
                self.state = "DEALER_PLAY"

            if player.busted:
                return "BUSTED"

            return "SUCCESS"
        else:
            return "NOT_PLAYERS_TURN"
