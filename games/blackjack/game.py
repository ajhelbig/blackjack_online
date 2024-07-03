from games.blackjack.player import *
from games.blackjack.dealer import *
from games.blackjack.deck import *
from client.client import *

class Game:

	def __init__(self, num_decks):
		self.game_id = id(self)
		self.clients = set()
		self.players = dict()
		self.dealer = Dealer()
		self.deck = Deck(num_decks=num_decks)
		self.round_start = False
		self.num_players = 0
		self.players_with_bets = 0

	def add_new_player(self, client):
		new_player = Player(client=client, bank=500)

		self.players[new_player.player_id] = new_player

		self.num_players += 1

		return f"{new_player.player_id}"
	
	def take_bet(self, player_id, bet):
		self.players[player_id].place_bet(bet_amount=bet)
		self.players_with_bets += 1

		if self.players_with_bets == self.num_players:
			self.round_start = True
	
	def broadcast(self, msg):
		for _, player in self.players.items():
			

	def deal_hands(self):
		for _, player in self.players.items():
			player.get_new_hand()

	def get_state():
		pass

	def start_round(self):
		pass



