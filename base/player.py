class Player:
    def __init__(self, name, bank):
        self.bank = bank
        self.name = name
        self.bet = None
        self.hands = []
        self.active_hand = ""