import os
from base.client import Client
import pygame
import pygame_menu

class Game_Client(Client):

    def __init__(self, s=None):
        
        super().__init__(s=s)

        self.game_id = ""
        self.player_id = ""
        self.name = str()
        self.players = list()
        self.player_hands = list()
        self.dealer_hands = list()

        self.window_size = (1200, 800)
        self.menu_x_scale_factor = 0.5
        self.menu_y_scale_factor = 0.5
        self.bg = pygame.image.load('assets/images/bg.png')
        self.bg = pygame.transform.scale(self.bg, self.window_size)

        pygame.init()

        self.window = pygame.display.set_mode(self.window_size, pygame.RESIZABLE)

        self.sign_in_menu = pygame_menu.Menu('Sign In',
                                        self.window_size[0] * self.menu_x_scale_factor, 
                                        self.window_size[1] * self.menu_y_scale_factor,
                                        theme=pygame_menu.themes.THEME_DARK)
        
        self.create_account_menu = pygame_menu.Menu('Create Account',
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
        self.sign_in_menu.add.button('Sign In', self.sign_in)
        self.sign_in_menu.add.button('Create Account', self.create_account_menu)
        self.sign_in_menu.add.button('Forgot Password', None)# implement account recovery later

        self.create_account_menu.add.label(title='', label_id='create account messager', wordwrap=True)
        self.create_account_menu.add.text_input('Username: ', textinput_id='create account username')
        self.create_account_menu.add.text_input('Recovery Email: ', textinput_id='create account email')
        self.create_account_menu.add.text_input('Password: ', textinput_id='create account 1st password')
        self.create_account_menu.add.text_input('Password: ', textinput_id='create account 2nd password')
        self.create_account_menu.add.button('Create Account', self.create_account)

        self.main_menu.add.button('Start Game', self.start_game)
        self.main_menu.add.button('Join Game', self.join_menu)
        self.main_menu.add.button('Quit', pygame_menu.events.EXIT)

        self.join_menu.add.text_input('Game ID: ')
        self.join_menu.add.button('Join', self.join_game)

        self.menus = [self.sign_in_menu, self.main_menu, self.join_menu]
        self.current_menu = self.sign_in_menu

    def join_game(self):
        print('join')
        pass

    def start_game(self):
        print("start")
        pass

    def sign_in(self):
        username = self.sign_in_menu.get_widget('username').get_value()
        password = self.sign_in_menu.get_widget('password').get_value()
        display_msg = ''

        if not username or not password:
            display_msg = "A blank username or password won't work.\nTry again."

        else:
            server_msg = ['SIGN_IN', '3', 'SUCCESS', 'BAD_USER', 'BAD_PSWD', username, password]
            server_msg = ' '.join(server_msg)
            self.send_q.append(server_msg)
            ret = self.await_msg(server_msg)

            if ret == "SUCCESS":
                self.name = username
                self.current_menu = self.main_menu
                return
            elif ret == "BAD_USER":
                display_msg = 'There is no account with that username.\nTry creating an account.'
            elif ret == "BAD_PSWD":
                display_msg = 'That was not the right password'
            
        label = self.sign_in_menu.get_widget('sign in messager')
        label.set_title(display_msg)
        u = self.sign_in_menu.get_widget('username')
        p = self.sign_in_menu.get_widget('password')
        u.clear()
        p.clear()

    def create_account(self):
        username = self.create_account_menu.get_widget('create account username').get_value()
        email = self.create_account_menu.get_widget('create account email').get_value()
        password1 = self.create_account_menu.get_widget('create account 1st password').get_value()
        password2 = self.create_account_menu.get_widget('create account 2nd password').get_value()
        display_msg = ''

        if not username or not email or not password1 or not password2:
            display_msg = 'You must fill out all the text fields.'

        elif password1 != password2:
            display_msg = 'Both passwords must be the same.'

        else:
            server_msg = ['CREATE_ACCOUNT', '2', 'SUCCESS', 'USER_TAKEN', username, password1, email]
            server_msg = ' '.join(server_msg)
            self.send_q.append(server_msg)
            ret = self.await_msg(server_msg)

            if ret == "SUCCESS":
                self.name = username
                self.current_menu = self.main_menu
            elif ret == "USER_TAKEN":
                display_msg = 'That username is already taken.\nTry again.'

        label = self.create_account_menu.get_widget('create account messager')
        label.set_title(display_msg)
        u = self.create_account_menu.get_widget('create account username')
        e = self.create_account_menu.get_widget('create account email')
        p1 = self.create_account_menu.get_widget('create account 1st password')
        p2 = self.create_account_menu.get_widget('create account 2nd password')
        u.clear()
        e.clear()
        p1.clear()
        p2.clear()

    def resize_menus(self):
        new_window_size = self.window.get_size()

        for menu in self.menus:
            menu.resize(new_window_size[0] * self.menu_x_scale_factor, 
                        new_window_size[1] * self.menu_y_scale_factor)

    def play(self):
        stop = False
        while not stop:

            self.window.blit(self.bg, (0, 0))

            events = pygame.event.get()

            for event in events:

                if event.type == pygame.QUIT:
                    stop = True

                elif event.type == pygame.WINDOWSIZECHANGED:
                    self.bg = pygame.transform.scale(self.bg, self.window.get_size())
                    self.resize_menus()
                
            if self.current_menu.is_enabled():
                self.current_menu.update(events)
                self.current_menu.draw(self.window)

            pygame.display.update()

        #store state in db before exiting
        pygame.quit()

    def start(self):
        super().start()

        self.play()
