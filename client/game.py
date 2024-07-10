import pygame
import pygame_menu

class Game:

    def __init__(self):
        self.game_id = ""
        self.player_id = ""
        self.players = list()
        self.player_hands = list()
        self.dealer_hands = list()


    def join_game(self):
        print("join")
        pass

    def start_game(self):
        print("start")
        pass

    def play(self):
        # pygame setup
        pygame.init()
        surface = pygame.display.set_mode((600, 400))

        menu = pygame_menu.Menu('Blackjack', 400, 300,
                            theme=pygame_menu.themes.THEME_DARK)

        menu.add.text_input('Player Name: ', default='Ass Hoe')
        menu.add.button('Start Game', self.start_game)
        menu.add.button('Join Game', self.join_game)
        menu.add.button('Quit', pygame_menu.events.EXIT)

        menu.mainloop(surface)
        pygame.quit()