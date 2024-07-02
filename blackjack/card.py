
class Card:

	def __init__(self):
		self.value = 0
		self.suit = ""
		self.symbol = ""

	def stringify(self):

		return f"{self.value} {self.suit} {self.symbol},"