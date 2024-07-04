from client.client import *
from client.game_instance import *
from assets.text import *

c = Client()
c.connect('10.0.0.8', 5890)
g = Game_Instance()

while True: #menu loop

	choice = input(greeting)

	if choice == "join":

		game_id = input("Enter game id below.\nGame ID: ")

		c.send_msg(f"join {game_id}")
		msg_recv = c.recv_msg().split()
		print(msg_recv)
		break

	elif choice == "start":

		c.send_msg("start")
		msg_recv = c.recv_msg().split()	
		print(msg_recv)
		break

	print(invalid_input)

# while True:#game play loop
	
# 	bet = input(place_bet)

# 	try:
# 		float(bet)

# 	except:
# 		print(invalid_bet)
# 		break

# 	c.send_msg(f"{g.game_id} {g.player_id} bet {bet}")

# 	msg_recv = c.recv_msg()

# 	print(msg_recv)

# 	while msg_recv[0] != "round" and msg_recv[1] != "start":
# 		msg_recv = c.recv_msg().split()

# 	print(msg_recv)

# c.close_connection()
