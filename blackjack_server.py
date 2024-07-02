import socket
import threading
from client.client import *
from server.server import *
from blackjack.game import *

games = dict()

def respond_to_client(client_socket, address):

    c = Client(client_socket)

    msg = c.recv_msg()

    if msg == "start game":
        c.send_msg(create_new_game())
        
    elif msg == "join game":
        c.send_msg("joining game")

    else:
        c.send_msg("")

    c.close_connection()

def create_new_game():
    new_game = Game()
    games[new_game.game_id] = new_game
    new_player = new_game.add_new_player()

    return f"game id: {new_game.game_id}, player id: {new_player}"

s = Server(port=5890)

s.start(client_handler=respond_to_client)