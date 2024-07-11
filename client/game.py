import pygame
import pygame_menu

class Game:

    def __init__(self):
        self.game_id = ""
        self.player_id = ""
        self.players = list()
        self.player_hands = list()
        self.dealer_hands = list()

        self.window_size

        self.main_menu = pygame_menu.Menu('Break The Bank',
                                        400, 
                                        300,
                                        theme=pygame_menu.themes.THEME_DARK)
        self.join_menu = 



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

        main_menu = pygame_menu.Menu('Break The Bank', 400, 300,
                            theme=pygame_menu.themes.THEME_DARK)
        
        main_menu.add.text_input('Player Name: ', default='Ass Hoe')
        main_menu.add.button('Start Game', self.start_game)
        main_menu.add.button('Join Game', self.join_game)
        main_menu.add.button('Quit', pygame_menu.events.EXIT)
        
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()

            if main_menu.is_enabled():
                main_menu.mainloop(surface)

            pygame.display.flip()

        pygame.quit()