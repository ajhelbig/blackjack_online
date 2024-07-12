import pygame
import pygame_menu

class Game:

    def __init__(self, send_q, recv_q):
        self.game_id = ""
        self.player_id = ""
        self.name = str()
        self.players = list()
        self.player_hands = list()
        self.dealer_hands = list()

        self.send_q = send_q
        self.recv_q = recv_q

        self.window_size = (1200, 800)
        self.menu_x_scale_factor = 0.5
        self.menu_y_scale_factor = 0.5

        pygame.init()

        self.window = pygame.display.set_mode(self.window_size, pygame.RESIZABLE)

        self.start_menu = pygame_menu.Menu('What Should We Call You?',
                                        self.window_size[0] * self.menu_x_scale_factor, 
                                        self.window_size[1] * self.menu_y_scale_factor,
                                        theme=pygame_menu.themes.THEME_DARK)

        self.main_menu = pygame_menu.Menu('Break The Bank',
                                        self.window_size[0] * self.menu_x_scale_factor, 
                                        self.window_size[1] * self.menu_y_scale_factor,
                                        theme=pygame_menu.themes.THEME_DARK)

        self.join_menu = pygame_menu.Menu('Join A Game',
                                        self.window_size[0] * self.menu_x_scale_factor, 
                                        self.window_size[1] * self.menu_y_scale_factor,
                                        theme=pygame_menu.themes.THEME_DARK)

        self.start_menu.add.text_input('Username: ', textinput_id='username')
        self.start_menu.add.button('Continue', self.register_username)

        self.main_menu.add.button('Start Game', self.start_game)
        self.main_menu.add.button('Join Game', self.join_menu)
        self.main_menu.add.button('Quit', pygame_menu.events.EXIT)

        self.join_menu.add.text_input('Game ID: ')
        self.join_menu.add.button('Join', self.join_game)

        self.menus = [self.start_menu, self.main_menu, self.join_menu]
        self.current_menu = self.start_menu

    def join_game(self):
        print('join')
        pass

    def start_game(self):
        print("start")
        pass

    def register_username(self):
        username = self.start_menu.get_widget('username').get_value()
        username = 'REGISTER_USERNAME ' + username
        self.send_q.append(username)
        ret = str()

        while True:
            try:
                ret = self.recv_q.pop(0)
                
                if ret == "SUCCESS":
                    self.name = username
                    self.current_menu = self.main_menu
                    break
                elif ret == "TAKEN":
                    print(ret)
                    break
                else:
                    self.recv_q.append(0)
            except:
                pass

    def resize_menus(self):
        new_window_size = self.window.get_size()

        for menu in self.menus:
            menu.resize(new_window_size[0] * self.menu_x_scale_factor, 
                        new_window_size[1] * self.menu_y_scale_factor)

    def play(self):

        while True:

            events = pygame.event.get()

            for event in events:

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == pygame.WINDOWSIZECHANGED:
                    self.resize_menus()
                
            if self.current_menu.is_enabled():
                self.current_menu.update(events)
                self.current_menu.draw(self.window)

            pygame.display.update()

        pygame.quit()