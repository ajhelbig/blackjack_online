
class Hand:

	def __init__(self, cards):
		self.cards = cards

	def stringify(self):
		hand = str()
		for card in self.cards:
			hand += " " + card.stringify() + " "

		return hand
		