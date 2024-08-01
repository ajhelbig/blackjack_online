from blackjack.player import Blackjack_Player

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
        ret_msg = {"code": None, 
                   "data": {"msg": None, 
                            "game_state": self.state}}
        
        player = self.players[username]

        if player.bet is not None:
            ret_msg["code"] = "FAIL"
            ret_msg["data"]["msg"] = "Bet has already been placed."
        else:
            player.place_bet(bet)
            self.bets_placed += 1
            ret_msg["code"] = "SUCCESS"

            if self.bets_placed < self.num_players:
                ret_msg["data"]["msg"] = "Bet has been placed. Waiting for other players to bet."
            else:
                #TODO deal cards to everyone
                self.state = "PLAY"
                ret_msg["data"]["msg"] = "Bet has been placed."
                ret_msg["data"]["game_state"] = self.state
        
        return ret_msg

    def hit(self, username):
        pass

    def stand(self, username):
        pass

    def double_down(self, username):
        pass
