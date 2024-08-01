
class Card:

	def __init__(self):
		self.value = 0
		self.suit = ""
		self.symbol = ""

	def soft_ace(self):
		self.value = 1

	def stringify(self):

		return f"{self.symbol}_of_{self.suit}"