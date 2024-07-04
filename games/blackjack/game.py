from games.blackjack.player import *
from games.blackjack.dealer import *
from games.blackjack.deck import *

class Game:

	def __init__(self, num_decks):
		self.game_id = id(self)
		self.players = dict()
		self.dealer = Dealer()
		self.deck = Deck(num_decks=num_decks)
		self.round_start = False
		self.num_players = 0
		self.bets_placed = 0

	def add_new_player(self):
		new_player = Player(bank=500)
		self.players[new_player.player_id] = new_player
		self.num_players += 1

		return f"{new_player.player_id}"
	
	def take_bet(self, player_id, bet):
		self.players[player_id].place_bet(bet_amount=bet)
		self.bets_placed += 1

		if self.bets_placed == self.num_players:
			self.round_start = True
	
	def broadcast(self, msg):
		pass
			

	def deal_hands(self):
		for _, player in self.players.items():
			player.get_new_hand()

	def get_state():
		pass

	def start_round(self):
		pass



