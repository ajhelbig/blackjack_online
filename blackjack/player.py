from blackjack.hand import *

class Player:

	def __init__(self, name, bank):
		self.bank = bank
		self.name = name
		self.bet = 0
		self.hands = []
		self.active_hand = ""

	def get_new_hand(self, deck):
		self.hands = []
		
		for i in range(2):
			self.hands.append(deck.pop())

	def place_bet(self, bet_amount):
		self.bet = float(bet_amount)

	def hit(self):
		pass

	def stand(self):
		pass

	def split(self):
		pass

	def insurance(self):
		pass

	def double_down(self):
		pass

	def surrender(self):
		pass

