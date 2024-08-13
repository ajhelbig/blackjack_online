import pygame_menu
import pygame_menu.themes

class UI:

    def __init__(self, window, sign_in, create_account, start_game,\
                join_game, pause_leave_game, pause_resume, place_bet,\
                double_down, hit, stand):

        self.window = window
        self.window_size = window.get_size()
        self.menu_x_scale_factor = 0.65
        self.menu_y_scale_factor = 0.65

        self.default_game_message = 'This is where messages will appear.'

        self.sign_in_menu = pygame_menu.Menu('Sign In',
                                        self.window_size[0] * self.menu_x_scale_factor, 
                                        self.window_size[1] * self.menu_y_scale_factor,
                                        theme=pygame_menu.themes.THEME_DARK)
        
        self.create_account_menu = pygame_menu.Menu('Create Account',
                                        self.window_size[0] * self.menu_x_scale_factor, 
                                        self.window_size[1] * self.menu_y_scale_factor,
                                        theme=pygame_menu.themes.THEME_DARK)

        self.main_menu = pygame_menu.Menu('Blackjack',
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

        self.game_menu = pygame_menu.Menu('Blackjack',
                                        self.window_size[0], 
                                        self.window_size[1],
                                        theme=pygame_menu.themes.THEME_DARK,
                                        overflow=False)

        self.sign_in_menu.add.label(title='', label_id='sign in messager', wordwrap=True)
        self.sign_in_menu.add.text_input('Username: ', textinput_id='username')
        self.sign_in_menu.add.text_input('Password: ', textinput_id='password', password=True)
        self.sign_in_menu.add.button('Sign In', sign_in)
        self.sign_in_menu.add.button('Create Account', self.create_account_menu)
        self.sign_in_menu.add.button('Quit', pygame_menu.events.EXIT)

        self.create_account_menu.add.label(title='', label_id='create account messager', wordwrap=True)
        self.create_account_menu.add.text_input('Username: ', textinput_id='create account username')
        self.create_account_menu.add.text_input('Password: ', textinput_id='create account 1st password')
        self.create_account_menu.add.text_input('Password: ', textinput_id='create account 2nd password')
        self.create_account_menu.add.button('Create Account', create_account)
        self.create_account_menu.add.button('Quit', pygame_menu.events.EXIT)

        self.main_menu.add.button('Start Game', self.start_menu)
        self.main_menu.add.button('Join Game', self.join_menu)
        self.main_menu.add.button('Quit', pygame_menu.events.EXIT)

        self.join_menu.add.label('', label_id='join game messager', wordwrap=True)
        self.join_menu.add.text_input('Game Name: ', textinput_id='join game name')
        self.join_menu.add.text_input('Optional - Game Password: ', textinput_id='join game password')
        self.join_menu.add.button('Join', join_game)

        self.start_menu.add.label(title='', label_id='start game messager', wordwrap=True)
        self.start_menu.add.text_input('Game Name: ', textinput_id='start game name')
        self.start_menu.add.text_input('Optional - Game Password: ', textinput_id='start game password')
        self.start_menu.add.button('Start Game', start_game)

        self.pause_menu.add.button('Resume', pause_resume)
        self.pause_menu.add.button('Leave Game', pause_leave_game)

        self.game_menu.add.label(title=self.default_game_message, label_id='game messager', wordwrap=True)
        self.game_menu.add.image(image_path='assets/images/game_bg.jpg', image_id='game background')
        self.game_menu.add.text_input('Bet Ammount: ', textinput_id='bet text')
        self.game_menu.add.button(title='Place Bet', action=place_bet, button_id='bet button')

        frame = self.game_menu.add.frame_h(width=self.window_size[0], 
                                           height=self.window_size[1] * 0.1, 
                                           frame_id='play buttons',
                                           margin=(0,0))

        frame.pack(widget=self.game_menu.add.button(title='Double Down', action=double_down, button_id='double down button'), align='align-center', vertical_position='position-center', margin=(50,0))
        frame.pack(widget=self.game_menu.add.button(title='Hit', action=hit, button_id='hit button'), align='align-center', vertical_position='position-center', margin=(50,0))
        frame.pack(widget=self.game_menu.add.button(title='Stand', action=stand, button_id='stand button'), align='align-center', vertical_position='position-center', margin=(50,0))

        bet_text = self.game_menu.get_widget('bet text')
        bet_text.hide()
        bet_button = self.game_menu.get_widget('bet button')
        bet_button.hide()

        frame.hide()

        self.game_menu.set_absolute_position(0, 0)

        self.current_menu = self.sign_in_menu

        self.menus = [self.sign_in_menu, 
                      self.create_account_menu, 
                      self.main_menu,
                      self.join_menu,
                      self.start_menu,
                      self.pause_menu,
                      self.game_menu]
        
        self.resize(self.window_size)

    def get_bet_values(self):
        bet_amount = self.game_menu.get_widget('bet text').get_value()
        return bet_amount
    
    def set_bet_values(self):
        bet = self.game_menu.get_widget('bet text')
        bet.clear()

    def set_game_inputs(self, state):
        if state == "BET":
            bet_text = self.game_menu.get_widget('bet text')
            bet_text.show()
            bet_button = self.game_menu.get_widget('bet button')
            bet_button.show()
        
        elif state == "PLAY":
            bet_text = self.game_menu.get_widget('bet text')
            bet_text.hide()
            bet_button = self.game_menu.get_widget('bet button')
            bet_button.hide()

            play_buttons = self.game_menu.get_widget('play buttons')
            play_buttons.show()
        else:
            bet_text = self.game_menu.get_widget('bet text')
            bet_text.hide()
            bet_button = self.game_menu.get_widget('bet button')
            bet_button.hide()
            play_buttons = self.game_menu.get_widget('play buttons')
            play_buttons.hide()

    def set_game_message(self, msg=None):
        if msg is None:
            msg = self.default_game_message
        
        game_messager = self.game_menu.get_widget('game messager')
        game_messager.set_title(msg)

    def resize(self, window_size):
        for menu in self.menus:
            menu.resize(window_size[0] * self.menu_x_scale_factor, 
                        window_size[1] * self.menu_y_scale_factor)
            
        self.game_menu.resize(window_size[0], window_size[1])
        self.game_menu.set_absolute_position(0, 0)
        bg = self.game_menu.get_widget('game background')
        bg.resize(window_size[0], window_size[1] * 0.75)

    def switch_to_pause_menu(self):
        self.current_menu = self.pause_menu

    def switch_to_game_menu(self, state, msg=None):
        self.set_game_message(msg)
        self.set_game_inputs(state)
        self.current_menu = self.game_menu

    def switch_to_main_menu(self):
        self.current_menu = self.main_menu

    def draw(self, events):
        try:
            if self.current_menu.is_enabled():
                self.current_menu.update(events)
                self.current_menu.draw(self.window)
        except:
            pass
        
    def get_sign_in_values(self):
        username = self.sign_in_menu.get_widget('username').get_value()
        password = self.sign_in_menu.get_widget('password').get_value()

        return username, password
    
    def set_sign_in_values(self, display_msg):
        label = self.sign_in_menu.get_widget('sign in messager')
        label.set_title(display_msg)
        u = self.sign_in_menu.get_widget('username')
        p = self.sign_in_menu.get_widget('password')
        u.clear()
        p.clear()

    def get_create_account_values(self):
        username = self.create_account_menu.get_widget('create account username').get_value()
        password1 = self.create_account_menu.get_widget('create account 1st password').get_value()
        password2 = self.create_account_menu.get_widget('create account 2nd password').get_value()

        return username, password1, password2
    
    def set_create_account_values(self, display_msg):
        label = self.create_account_menu.get_widget('create account messager')
        label.set_title(display_msg)
        u = self.create_account_menu.get_widget('create account username')
        p1 = self.create_account_menu.get_widget('create account 1st password')
        p2 = self.create_account_menu.get_widget('create account 2nd password')
        u.clear()
        p1.clear()
        p2.clear()
    
    def get_start_game_values(self):
        gamename = self.start_menu.get_widget('start game name').get_value()
        game_password = self.start_menu.get_widget('start game password').get_value()

        return gamename, game_password
    
    def set_start_game_values(self, display_msg):
        label = self.start_menu.get_widget('start game messager')
        label.set_title(display_msg)
        u = self.start_menu.get_widget('start game name')
        p = self.start_menu.get_widget('start game password')
        u.clear()
        p.clear()

    def get_join_game_values(self):
        gamename = self.join_menu.get_widget('join game name').get_value()
        game_password = self.join_menu.get_widget('join game password').get_value()

        return gamename, game_password
    
    def set_join_game_values(self, display_msg):
        label = self.join_menu.get_widget('join game messager')
        label.set_title(display_msg)
        u = self.join_menu.get_widget('join game name')
        p = self.join_menu.get_widget('join game password')
        u.clear()
        p.clear()