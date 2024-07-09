from client.client import *
import pygame
# from client.game_instance import *
# from assets.text import *

c = Client()
c.connect('10.0.0.5', 5890)
c.start()

# initializing the constructor  
pygame.init()  
  
# screen resolution  
res = (720,720)  
  
# opens up a window  
screen = pygame.display.set_mode(res)  
  
# white color  
color = (255,255,255)  
  
# light shade of the button  
color_light = (170,170,170)  
  
# dark shade of the button  
color_dark = (100,100,100)  
  
# stores the width of the  
# screen into a variable  
width = screen.get_width()  
  
# stores the height of the  
# screen into a variable  
height = screen.get_height()  
  
# defining a font  
smallfont = pygame.font.SysFont('Corbel',35)  
  
# rendering a text written in  
# this font  
text = smallfont.render('quit' , True , color)  
  
while True:  
      
    for ev in pygame.event.get():  
          
        if ev.type == pygame.QUIT:  
            pygame.quit()  
              
        #checks if a mouse is clicked  
        if ev.type == pygame.MOUSEBUTTONDOWN:  
              
            #if the mouse is clicked on the  
            # button the game is terminated  
            if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40:  
                pygame.quit()  
                  
    # fills the screen with a color  
    screen.fill((60,25,60))  
      
    # stores the (x,y) coordinates into  
    # the variable as a tuple  
    mouse = pygame.mouse.get_pos()
      
    # if mouse is hovered on a button it  
    # changes to lighter shade  
    if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40:  
        pygame.draw.rect(screen,color_light,[width/2,height/2,140,40])  
          
    else:  
        pygame.draw.rect(screen,color_dark,[width/2,height/2,140,40])  
      
    # superimposing the text onto our button  
    screen.blit(text , (width/2+50,height/2))  
      
    # updates the frames of the game  
    pygame.display.update()


# g = Game_Instance()

# while True: #Menu loop

# 	try:
# 		choice = input(greeting)
# 	except KeyboardInterrupt:
# 		print(exit_msg, flush=True)
# 		exit()

# 	if choice == "join":

# 		try:
# 			game_id = input(enter_game_id)
# 		except KeyboardInterrupt:
# 			print(exit_msg, flush=True)
# 			exit()

# 		if game_id == "back":
# 			continue

# 		c.send_msg(f"join {game_id}")
# 		msg_recv = c.recv_msg().split()

# 		while msg_recv[-1] != "success":
# 			print(invalid_game_id)

# 			try:
# 				game_id = input(enter_game_id)
# 			except KeyboardInterrupt:
# 				print(exit, flush=True)
# 				exit()

# 			if game_id == "back":
# 				break

# 			c.send_msg(f"join {game_id}")
# 			msg_recv = c.recv_msg().split()

# 		if msg_recv[-1] == "success":
# 			print("You have joined the game successfully!")
# 			g.game_id = msg_recv[0]
# 			g.player_id = msg_recv[1]
# 			break

# 	elif choice == "start":

# 		c.send_msg("start")
# 		msg_recv = c.recv_msg().split()
		
# 		if msg_recv[-1] == "success":
# 			print(f"Your Game ID is: {msg_recv[0]}")
# 			g.game_id = msg_recv[0]
# 			g.player_id = msg_recv[1]
# 			break

# while True: #Game play loop
	
# 	try:
# 		bet = input(place_bet)
# 	except KeyboardInterrupt:
# 		print(exit_msg, flush=True)
# 		exit()

# 	try:
# 		float(bet)

# 	except:
# 		print(invalid_bet)
# 		continue

# 	c.send_msg(f"{g.game_id} {g.player_id} bet {bet}")
# 	msg_recv = c.recv_msg()
# 	print(msg_recv)
# 	break

# c.close_connection()
