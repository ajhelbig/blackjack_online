
class Hand:

	def __init__(self, deck):
		self.cards = []
		self.value = 0
		self.is_bust = False

		for _ in range(2):
			self.cards.append(deck.pop())

		self.update_hand_value()

	def add_card(self, deck):
		self.cards.append(deck.pop())
		self.update_hand_value()

	def update_hand_value(self):
		card_values = 0
		aces = []

		for card in self.cards:
			if card.symbol == 'ace':
				aces.append(card)
				card.is_soft_ace()

			card_values += card.value
		
		if card_values > 21:
			self.is_bust = True

		elif card_values < 21 and len(aces) > 0:
			for ace in aces:
				if card_values + 10 <= 21:
					card_values += 10
					ace.is_hard_ace()

		self.value = card_values

	def stringify(self):
		hand = str()
		for card in self.cards:
			hand += " " + card.stringify() + " "

		return hand
		