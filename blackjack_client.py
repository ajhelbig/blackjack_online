from client import *

greeting = f"Hello welcome to Blackjack!\nWould you like to join a game or start a game?\nEnter 'join' to join or 'start' to start!\n"

text = input(greeting)

c = ClientSocket()
c.connect('127.0.0.1', 5890)
game_on = False
game_info = ''

while True:

	if text == "join":

		c.c_send("join game\0")
		game_info = c.c_recv()

		#check if game info received is good if not retry
		
		game_on = True
		c.c_close()
		break

	elif text == "start":

		c.c_send("start game\0")
		game_info = c.c_recv()

		#check if game info received is good if not retry

		game_on = True
		c.c_close()
		break

	else:

		text = input(greeting)

print(game_info)
