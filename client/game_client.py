from base.client import Client
import pygame
import pygame_menu

class Game_Client(Client):

    def __init__(self, s=None):
        
        super().__init__(s=s)

        self.gamename = str()
        self.username = str()
        self.bank = str()
        self.players = list()
        self.player_hands = list()
        self.dealer_hands = list()
        self.active_game = False

        self.window_size = (1400, 1000)
        self.menu_x_scale_factor = 0.65
        self.menu_y_scale_factor = 0.65
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
        
        self.start_menu = pygame_menu.Menu('Start A Game',
                                        self.window_size[0] * self.menu_x_scale_factor, 
                                        self.window_size[1] * self.menu_y_scale_factor,
                                        theme=pygame_menu.themes.THEME_DARK)
        
        self.pause_menu = pygame_menu.Menu('Pause',
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

        self.main_menu.add.button('Start Game', self.start_menu)
        self.main_menu.add.button('Join Game', self.join_menu)
        self.main_menu.add.button('Quit', pygame_menu.events.EXIT)

        self.join_menu.add.label('', label_id='join game messager')
        self.join_menu.add.text_input('Game Name: ', textinput_id='join game name')
        self.join_menu.add.text_input('Optional - Game Password: ', textinput_id='join game password')
        self.join_menu.add.button('Join', self.join_game)

        self.start_menu.add.label(title='', label_id='start game messager', wordwrap=True)
        self.start_menu.add.text_input('Game Name: ', textinput_id='start game name')
        self.start_menu.add.text_input('Optional - Game Password: ', textinput_id='start game password')
        self.start_menu.add.button('Start Game', self.start_game)

        self.pause_menu.add.button('Resume', self.pause_resume)
        self.pause_menu.add.button('Quit', pygame_menu.events.EXIT)#TODO sync user with db

        self.menus = [self.sign_in_menu, self.create_account_menu, self.main_menu, self.join_menu, self.start_menu, self.pause_menu]
        self.current_menu = self.sign_in_menu

    def pause_resume(self):
        self.current_menu = None

    def pause_quit(self):
        pass

    def join_game(self):
        gamename = self.join_menu.get_widget('join game name').get_value().split()
        gamename = '$'.join(gamename)
        game_password = self.join_menu.get_widget('join game password').get_value()
        display_msg = ''

        if not game_password:
            game_password = "NULL"

        if not gamename:
            display_msg = "A blank game name won't work.\nTry again."
        else:
            server_msg = ['JOIN_GAME_TYPE_0', '4', 'SUCCESS', 'BAD_GAME_NAME', 'BAD_GAME_PSWD', 'GAME_FULL', self.username, gamename, game_password]
            server_msg = ' '.join(server_msg)
            self.send_q.append(server_msg)
            ret_val = self.await_msg(server_msg).split()

            if ret_val[0] == 'SUCCESS':
                self.current_menu = None
                self.gamename = gamename
                self.bg = pygame.image.load('assets/images/bg2.jpg')
                self.bg = pygame.transform.scale(self.bg, self.window_size)

            elif ret_val[0] == 'BAD_GAME_NAME':
                display_msg = "That game does not exist.\nTry again."

            elif ret_val[0] == 'BAD_GAME_PSWD':
                display_msg = 'That was the wrong password.\nTry again.'

            elif ret_val[0] == 'GAME_FULL':
                display_msg = "You can't join right now the game is full."

        label = self.join_menu.get_widget('join game messager')
        label.set_title(display_msg)
        u = self.join_menu.get_widget('join game name')
        p = self.join_menu.get_widget('join game password')
        u.clear()
        p.clear()

    def start_game(self):
        gamename = self.start_menu.get_widget('start game name').get_value().split()
        gamename = '$'.join(gamename)
        game_password = self.start_menu.get_widget('start game password').get_value()
        display_msg = ''

        if not game_password:
            game_password = "NULL"

        if not gamename:
            display_msg = "A blank game name won't work.\nTry again."
        else:
            server_msg = ['START_GAME_TYPE_0', '2', 'SUCCESS', 'BAD_GAME_NAME', self.username, gamename, game_password]
            server_msg = ' '.join(server_msg)
            self.send_q.append(server_msg)
            ret_val = self.await_msg(server_msg).split()

            if ret_val[0] == "SUCCESS":
                self.current_menu = None
                self.gamename = gamename
                self.bg = pygame.image.load('assets/images/bg2.jpg')
                self.bg = pygame.transform.scale(self.bg, self.window_size)
                
            elif ret_val[0] == "BAD_GAME_NAME":
                display_msg = 'Sorry that game name is already taken.\nTry again'

        label = self.start_menu.get_widget('start game messager')
        label.set_title(display_msg)
        u = self.start_menu.get_widget('start game name')
        p = self.start_menu.get_widget('start game password')
        u.clear()
        p.clear()

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
            ret_val = self.await_msg(server_msg).split()

            if ret_val[0] == "SUCCESS":
                self.username = username
                self.bank = int(ret_val[1])
                self.current_menu = self.main_menu
                return
            elif ret_val[0] == "BAD_USER":
                display_msg = 'There is no account with that username.\nTry creating an account.'
            elif ret_val[0] == "BAD_PSWD":
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
            ret_val = self.await_msg(server_msg).split()

            if ret_val[0] == "SUCCESS":
                self.username = username
                self.current_menu = self.main_menu
            elif ret_val[0] == "USER_TAKEN":
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
                
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.current_menu = self.pause_menu
            
            try:
                if self.current_menu.is_enabled():
                    self.current_menu.update(events)
                    self.current_menu.draw(self.window)
            except:
                pass

            pygame.display.update()

        #store state in db before exiting
        pygame.quit()
        exit()

    def start(self):
        super().start()

        self.play()