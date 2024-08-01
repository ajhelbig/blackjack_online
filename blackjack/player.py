from blackjack.hand import *
from base.player import Player

class Blackjack_Player(Player):

	def __init__(self, name, bank):
		super().__init__(name, bank)

	def get_new_hand(self, deck):
		self.hands = []
		new_hand = []

		for i in range(2):
			new_hand.append(deck.pop())
		
		self.hands.append(new_hand)

	def place_bet(self, bet_amount):
		self.bet = float(bet_amount)

	def hit(self):
		pass

	def stand(self):
		pass

	def double_down(self):
		pass
