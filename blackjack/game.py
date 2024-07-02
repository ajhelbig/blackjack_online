from blackjack.player import *
from blackjack.dealer import *
from blackjack.deck import *

class Game:

	def __init__(self):
		self.game_id = id(self)
		self.players = dict()
		self.dealer = Dealer()
		self.deck = Deck(num_decks=1)

	def add_new_player(self):
		new_player = Player()

		self.players[new_player.player_id] = new_player

		return f"{new_player.player_id}"