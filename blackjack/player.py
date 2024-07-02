
class Player:

	def __init__(self):
		self.player_id = id(self)
		self.bank = 0
		self.hands = list()
		self.active_hand = ""

	def get_new_hand(self, hand):
		self.hands = []
		self.hands.append(hand)

	def place_bet(self, bet_amount):
		pass

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

