from client import *

greeting = f"Hello welcome to Blackjack!\nWould you like to join a game or start a game?\nEnter 'join' to join or 'start' to start!\n"

text = input(greeting)

c = Client()
c.connect('127.0.0.1', 5890)
game_on = False
game_info = ''

while True:

	if text == "join":

		c.send_msg("join game\0")
		game_info = c.recv_msg()

		#check if game info received is good if not retry
		
		game_on = True
		c.close_connection()
		break

	elif text == "start":

		c.send_msg("start game\0")
		game_info = c.recv_msg()

		#check if game info received is good if not retry

		game_on = True
		c.close_connection()
		break

	else:

		text = input(greeting)

print(game_info)
