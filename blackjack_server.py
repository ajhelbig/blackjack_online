# from client.client import 
from server.server import *
# from games.blackjack.game import *

server = Server(port=5890)
server.start()

# games = dict()

# def respond_to_client(client_socket, address):

#     c = Client(client_socket)

#     while True:
#         try:
#             msg = c.recv_msg().split()
#         except RuntimeError:
#             print(f"{address} disconnected.")
#             break

#         if msg[0] == "start":
#             c.send_msg(create_new_game())
            
#         elif msg[0] == "join":
#             c.send_msg(join_game(msg))

#         elif msg[2] == "bet":
#             c.send_msg(take_bet(msg))

#         else:
#             c.send_msg("wtf was that")

#     c.close_connection()

# def create_new_game():
#     new_game = Game(num_decks=1)
#     games[new_game.game_id] = new_game
#     new_player_id = new_game.add_new_player()

#     print(f"Total players in GID {new_game.game_id} = {new_game.num_players}")

#     return f"{new_game.game_id} {new_player_id} success"

# def join_game(msg):
#     try:
#         game = games[msg[1]]
#         new_player_id = game.add_new_player()

#         print(f"Total players in GID {game.game_id} = {game.num_players}")

#         return f"{game.game_id} {new_player_id} success"
        
#     except KeyError:
#         return f"invalid"

# def take_bet(msg):
#     game = games[msg[0]]
#     game.take_bet(player_id=msg[1], bet=msg[3])
    
#     waiting_on = game.num_players - game.bets_placed

#     if waiting_on == 1:
#         return f"Your bet has been placed.\nWaiting for {waiting_on} player to place their bet..."
#     else:
#         return f"Your bet has been placed.\nWaiting for {waiting_on} players to place their bets..."
          
# s = Server(port=5890)
# s.start(client_handler=respond_to_client)
