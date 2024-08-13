from blackjack.card import *
from random import shuffle

suits = ["hearts", "diamonds", "clubs", "spades"]
symbols = ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "king", "queen"]
values = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

class Deck:

	def __init__(self, num_decks):
		self.cards = []
		self.played_cards = []

		for _ in range(num_decks):
			for suit in suits:
				for i in range(len(symbols)):

					new_card = Card()

					new_card.suit = suit
					new_card.symbol = symbols[i]
					new_card.value = values[i]

					self.cards.append(new_card)

		shuffle(self.cards)

	def pop(self):
		if len(self.cards) == 0:
			self.cards = self.played_cards
			shuffle(self.cards)
			self.played_cards = []

		self.played_cards.append(self.cards.pop(0))

		return self.played_cards[-1]

	def print_deck(self):
		for card in self.cards:
			print(card.stringify())

