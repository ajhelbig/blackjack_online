from client.client import *
from server.server import *
from games.blackjack.game import *

games = dict()

def respond_to_client(client_socket):

    c = Client(client_socket)

    msg = c.recv_msg().split()

    if msg[0] == "start":
        c.send_msg(create_new_game(client=c))
        
    elif msg[0] == "join":
        c.send_msg("joining game")

    elif msg[2] == "bet":
        take_bet(msg)

    else:
        c.send_msg("wtf was that")

def create_new_game(client):
    new_game = Game(num_decks=1)
    games[new_game.game_id] = new_game
    new_player = new_game.add_new_player(client=client)

    return f"{new_game.game_id} {new_player}"

def take_bet(msg):
    game = games[msg[0]]
    game.take_bet(player_id=msg[1], bet=msg[3])
    
    waiting_on = game.num_players - game.players_with_bets

    if waiting_on == 1:
        return f"Your bet has been placed.\nWaiting for {waiting_on} player to place their bet..."
    else:
        
        return f"Your bet has been placed.\nWaiting for {waiting_on} players to place their bets..."
          

s = Server(port=5890)

s.start(client_handler=respond_to_client)