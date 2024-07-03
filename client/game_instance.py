
class Game_Instance:

    def __init__(self):
        self.game_id = ""
        self.player_id = ""
        self.player_hands = list()
        self.dealer_hands = list()

    def start_round(self, new_hand):
        pass


    def print_instance(self):
        print(f"game id: {self.game_id}, player id: {self.player_id}")