
class Card:

	def __init__(self):
		self.value = 0
		self.suit = ""
		self.symbol = ""

	def is_soft_ace(self):
		self.value = 1

	def is_hard_ace(self):
		self.value = 11

	def stringify(self):
		return f"{self.symbol}_of_{self.suit}"