import pygame
import pygame_menu

class Game:

    def __init__(self):
        self.game_id = ""
        self.player_id = ""
        self.players = list()
        self.player_hands = list()
        self.dealer_hands = list()

        self.window_size = (1200, 800)
        self.menu_x_scale_factor = 0.5
        self.menu_y_scale_factor = 0.5

        pygame.init()

        self.window = pygame.display.set_mode(self.window_size, pygame.RESIZABLE)

        self.main_menu = pygame_menu.Menu('Break The Bank',
                                        self.window_size[0] * self.menu_x_scale_factor, 
                                        self.window_size[1] * self.menu_y_scale_factor,
                                        theme=pygame_menu.themes.THEME_DARK)

        self.join_menu = pygame_menu.Menu('Join A Game',
                                        self.window_size[0] * self.menu_x_scale_factor, 
                                        self.window_size[1] * self.menu_y_scale_factor,
                                        theme=pygame_menu.themes.THEME_DARK)

        self.main_menu.add.button('Start Game', self.start_game)
        self.main_menu.add.button('Join Game', self.join_menu)
        self.main_menu.add.button('Quit', pygame_menu.events.EXIT)

        self.join_menu.add.text_input('Game ID: ')
        self.join_menu.add.button('Join', self.join_game)

    def join_game(self):
        print("join")
        pass

    def start_game(self):
        print("start")
        pass

    def play(self):

        while True:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == pygame.WINDOWRESIZED:
                    print("resized")

                elif event.type == pygame.WINDOWMAXIMIZED:
                    print('maximized')

                elif event.type == pygame.WINDOWSIZECHANGED:
                    print('changed')

            if self.main_menu.is_enabled():
                self.main_menu.mainloop(self.window)

            pygame.display.update()

        pygame.quit()