from games.blackjack.card import *
from random import shuffle

suits = ["H", "D", "C", "S"]
symbols = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "K", "Q"]
values = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

class Deck:

	def __init__(self, num_decks):
		self.cards = list()
		self.played_cards = list()

		for _ in range(num_decks):
			for suit in suits:
				for i in range(len(symbols)):

					new_card = Card()

					new_card.suit = suit
					new_card.symbol = symbols[i]
					new_card.value = values[i]

					self.cards.append(new_card)

	def shuffle(self):
		shuffle(self.cards)

	def pop(self):
		if len(self.cards) == 0:
			self.cards = self.played_cards
			self.shuffle()
			self.played_cards = list()

		self.played_cards.append(self.cards.pop(0))

		return self.played_cards[-1]

	def print_deck(self):
		for card in self.cards:
			print(card.stringify())

