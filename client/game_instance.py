import pygame
import sys
from assets.colors import *

class Game_Instance:

    def __init__(self):
        self.game_id = ""
        self.player_id = ""
        self.players = list()
        self.player_hands = list()
        self.dealer_hands = list()
          
        pygame.init()

        self.res = (720,720)
        self.screen = pygame.display.set_mode(self.res)
        self.width = self.screen.get_width()  
        self.height = self.screen.get_height()
        self.smallfont = pygame.font.SysFont('Corbel',35) 
        self.text = self.smallfont.render('quit' , True , color)

    def play(self):

        msg = ""
      
        for ev in pygame.event.get():  
            
            if ev.type == pygame.QUIT:  
                pygame.quit()  
                    
            if ev.type == pygame.MOUSEBUTTONDOWN:  
                    
                if self.width/2 <= mouse[0] <= self.width/2+140 and self.height/2 <= mouse[1] <= self.height/2+40:  
                    pygame.quit()
                        
        self.screen.fill((60,25,60))  
            
        mouse = pygame.mouse.get_pos()
        
        if self.width/2 <= mouse[0] <= self.width/2+140 and self.height/2 <= mouse[1] <= self.height/2+40:  
            pygame.draw.rect(self.screen,color_light,[self.width/2,self.height/2,140,40])  
            
        else:  
            pygame.draw.rect(self.screen,color_dark,[self.width/2,self.height/2,140,40])  
            
        self.screen.blit(self.text , (self.width/2, self.height/2))  
        
        pygame.display.update()

        return msg

    def start_round(self, new_hand):
        pass


    def print_instance(self):
        print(f"game id: {self.game_id}, player id: {self.player_id}")