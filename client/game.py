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

        self.sign_in_menu = pygame_menu.Menu('Sign In',
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

        self.sign_in_menu.add.label(title='', label_id='sign in messager', wordwrap=True)
        self.sign_in_menu.add.text_input('Username: ', textinput_id='username')
        self.sign_in_menu.add.text_input('Password: ', textinput_id='password', password=True)
        self.sign_in_menu.add.button('Continue', self.sign_in)

        self.main_menu.add.button('Start Game', self.start_game)
        self.main_menu.add.button('Join Game', self.join_menu)
        self.main_menu.add.button('Quit', pygame_menu.events.EXIT)

        self.join_menu.add.text_input('Game ID: ')
        self.join_menu.add.button('Join', self.join_game)

        self.menus = [self.sign_in_menu, self.main_menu, self.join_menu]
        self.current_menu = self.sign_in_menu
    
    def recv_msg(self, responses):
        resp = str()
        while True:
            try:
                resp = self.recv_q.pop(0)
                if resp in responses:
                    return resp
                else:
                    self.recv_q.append(resp)
            except:
                pass

    def send_msg(self, code, msg):
        final_msg = code + ' ' + msg
        self.send_q.append(final_msg)

    def join_game(self):
        print('join')
        pass

    def start_game(self):
        print("start")
        pass

    def sign_in(self):
        username = self.sign_in_menu.get_widget('username').get_value()
        password = self.sign_in_menu.get_widget('password').get_value()

        if not username or not password:
            label = self.sign_in_menu.get_widget('sign in messager')
            label.set_title("A blank username or password won't work.\nTry again.")
            u = self.sign_in_menu.get_widget('username')
            p = self.sign_in_menu.get_widget('password')
            u.clear()
            p.clear()

        else:
            self.send_msg('SIGN_IN', username + ' ' + password)

            options = ["SUCCESS", "FAIL"]
            ret = self.recv_msg(options)

            if ret == "SUCCESS":
                self.name = username
                self.current_menu = self.main_menu
            else:
                label = self.sign_in_menu.get_widget('sign in messager')
                label.set_title("The username or password is incorrect.")
                u = self.sign_in_menu.get_widget('username')
                p = self.sign_in_menu.get_widget('password')
                u.clear()
                p.clear()

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