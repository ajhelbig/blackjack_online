from client.client import *
from client.game_instance import *
from assets.text import *

c = Client()
c.connect('10.0.0.5', 5890)
g = Game_Instance()

while True: #Menu loop

	try:
		choice = input(greeting)
	except KeyboardInterrupt:
		print(exit_msg, flush=True)
		exit()

	if choice == "join":

		try:
			game_id = input(enter_game_id)
		except KeyboardInterrupt:
			print(exit_msg, flush=True)
			exit()

		if game_id == "back":
			continue

		c.send_msg(f"join {game_id}")
		msg_recv = c.recv_msg().split()

		while msg_recv[-1] != "success":
			print(invalid_game_id)

			try:
				game_id = input(enter_game_id)
			except KeyboardInterrupt:
				print(exit, flush=True)
				exit()

			if game_id == "back":
				break

			c.send_msg(f"join {game_id}")
			msg_recv = c.recv_msg().split()

		if msg_recv[-1] == "success":
			print("You have joined the game successfully!")
			g.game_id = msg_recv[0]
			g.player_id = msg_recv[1]
			break

	elif choice == "start":

		c.send_msg("start")
		msg_recv = c.recv_msg().split()
		
		if msg_recv[-1] == "success":
			print(f"Your Game ID is: {msg_recv[0]}")
			g.game_id = msg_recv[0]
			g.player_id = msg_recv[1]
			break

while True: #Game play loop
	
	try:
		bet = input(place_bet)
	except KeyboardInterrupt:
		print(exit_msg, flush=True)
		exit()

	try:
		float(bet)

	except:
		print(invalid_bet)
		continue

	c.send_msg(f"{g.game_id} {g.player_id} bet {bet}")
	msg_recv = c.recv_msg()
	print(msg_recv)
	break

c.close_connection()
