from blackjack.hand import Hand
from base.player import Player

class Blackjack_Player(Player):

	def __init__(self, name, bank):
		super().__init__(name, bank)
		self.state = None
		self.busted = False

	def get_new_hand(self, deck):
		self.state = "PLAYABLE"
		self.hands = []
		self.hands.append(Hand(deck))

	def place_bet(self, bet_amount):
		self.bet = float(bet_amount)

	def hit(self, deck, hand_index=0):
		self.hands[hand_index].add_card(deck)
		self.busted = self.hands[hand_index].is_bust

	def stand(self):
		self.state = "NOT_PLAYABLE"

	def double_down(self, deck):
		self.bet *= 2
		self.hit(deck)
