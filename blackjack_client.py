from client.client import *

greeting = f"Hello welcome to Blackjack!\nWould you like to join a game or start a game?\nEnter 'join' to join or 'start' to start!\n"

text = input(greeting)

c = Client()
c.connect('127.0.0.1', 5890)

while True:

	if text == "join":

		c.send_msg("join game")
		msg_recv = c.recv_msg()

		#check if game info received is good if not retry

		print(msg_recv)
		break

	elif text == "start":

		c.send_msg("start game")
		msg_recv = c.recv_msg()

		#check if game info received is good if not retry
		
		print(msg_recv)
		break

	else:

		text = input(greeting)

c.close_connection()
