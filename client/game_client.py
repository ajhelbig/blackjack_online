import pygame
import json
from base.client import Client
from client.ui import UI

class Game_Client(Client):

    def __init__(self, s=None):
        
        super().__init__(s=s)
        
        self.in_game = False
        self.game_state = None
        self.gamename = None
        self.username = None
        self.bank = None
        self.current_menu = None
        self.active_inputs = None
        self.active_hand = None
        self.dealer = None
        self.players = []
        self.window_size = (1200, 1000)
        self.set_bg("MENU")

        pygame.init()

        self.window = pygame.display.set_mode(self.window_size, pygame.RESIZABLE)
        self.ui = UI(self.window,
                           self.sign_in,
                           self.create_account,
                           self.start_game,
                           self.join_game,
                           self.pause_leave_game,
                           self.pause_resume,
                           self.bet,
                           self.double_down,
                           self.hit,
                           self.stand)

    def pause_resume(self):
        self.ui.switch_to_game_menu("RESUME")

    def pause_leave_game(self):
        self.ui.switch_to_main_menu()
        self.leave_game()

    def sign_in(self):
        username, password = self.ui.get_sign_in_values()
        display_msg = ''

        if not username or not password:
            display_msg = "A blank username or password won't work.\nTry again."

        else:
            msg = {"code": "SIGN_IN", 
                   "response_codes": ["SUCCESS", "BAD_USER", "BAD_PSWD", "DUP_SIGN_IN"], 
                   "data": { "username": username, 
                             "password": password }
                    }
            
            resp = self.send_then_recv(msg)

            if resp["code"] == "SUCCESS":
                self.username = username
                self.bank = 0
                self.ui.switch_to_main_menu()

            elif resp["code"] == "BAD_USER":
                display_msg = 'There is no account with that username.\nTry creating an account.'

            elif resp["code"] == "BAD_PSWD":
                display_msg = 'That was not the right password.'

            elif resp["code"] == "DUP_SIGN_IN":
                display_msg = "You are already signed in."
            
        self.ui.set_sign_in_values(display_msg)

    def create_account(self):
        username, password1, password2 = self.ui.get_create_account_values()
        display_msg = ''

        if not username or not password1 or not password2:
            display_msg = 'You must fill out all the text fields.'

        elif password1 != password2:
            display_msg = 'Both passwords must be the same.'

        else:
            msg = {"code": "CREATE_ACCOUNT", 
                   "response_codes": ["SUCCESS", "USER_TAKEN"], 
                   "data": { "username": username, 
                             "password": password1 }
                    }
            
            resp = self.send_then_recv(msg)

            if resp["code"] == "SUCCESS":
                self.username = username
                self.bank = 0
                self.ui.switch_to_main_menu()

            elif resp["code"] == "USER_TAKEN":
                display_msg = 'That username is already taken.\nTry again.'

        self.ui.set_create_account_values(display_msg)

    def start_game(self):
        gamename, game_password = self.ui.get_start_game_values()
        display_msg = ''

        if not game_password:
            game_password = "NULL"

        if not gamename:
            display_msg = "A blank game name won't work.\nTry again."
        else:
            msg = {"code": "START_GAME", 
                   "response_codes": ["SUCCESS", "BAD_GAME_NAME"], 
                   "data": { "username": self.username, 
                             "gamename": gamename, 
                             "game_password": game_password }
                    }
            
            resp = self.send_then_recv(msg)

            if resp["code"] == "SUCCESS":
                self.gamename = gamename
                self.in_game = True
                self.game_state = resp["data"]["game_state"]
                self.bank = resp["data"]["starting_bank"]
                self.ui.switch_to_game_menu(self.game_state)

            elif resp["code"] == "BAD_GAME_NAME":
                display_msg = 'Sorry that game name is already taken.\nTry again'

        self.ui.set_start_game_values(display_msg)

    def join_game(self):
        gamename, game_password = self.ui.get_join_game_values()
        display_msg = ''

        if not game_password:
            game_password = "NULL"

        if not gamename:
            display_msg = "A blank game name won't work.\nTry again."
        else:
            msg = {"code": "JOIN_GAME", 
                   "response_codes": ["SUCCESS", "BAD_GAME_NAME", "BAD_GAME_PSWD", "GAME_FULL"], 
                   "data": { "username": self.username, 
                             "gamename": gamename, 
                             "game_password": game_password }
                   }
            
            resp = self.send_then_recv(msg)

            if resp["code"] == 'SUCCESS':
                self.gamename = gamename
                self.in_game = True
                self.game_state = resp["data"]["game_state"]
                self.bank = resp["data"]["starting_bank"]
                self.ui.switch_to_game_menu(self.game_state)

            elif resp["code"] == 'BAD_GAME_NAME':
                display_msg = "That game does not exist.\nTry again."

            elif resp["code"] == 'BAD_GAME_PSWD':
                display_msg = 'That was the wrong password.\nTry again.'

            elif resp["code"] == 'GAME_FULL':
                display_msg = "That game is full."

        self.ui.set_join_game_values(display_msg)

    def leave_game(self):
        msg = {"code": "LEAVE_GAME",
               "response_codes": ["SUCCESS", "FAIL"], 
               "data": { "username": self.username, 
                         "gamename": self.gamename }
                }
        
        resp = self.send_then_recv(msg)

        if resp["code"] == 'SUCCESS':
            self.ui.switch_to_main_menu()
            self.gamename = None
            self.in_game = False
            self.game_state = None
            self.bank = None

    def send_then_recv(self, json_dict):
        self.send_q.append(json.dumps(json_dict))
        return self.await_msg(json.dumps(json_dict))
    
    def set_bg(self, bg):
        path = None

        if bg == "MENU":
            path = 'assets/images/menu_bg.jpg'
        elif bg == "GAME":
            path = 'assets/images/game_bg.jpg'

        self.bg = pygame.image.load(path)
        self.bg = pygame.transform.scale(self.bg, self.window_size)

    def resize_ui(self):
        self.window_size = self.window.get_size()
        self.ui.resize(self.window_size)
        
    def draw_dealer_cards(self):
        pass

    def draw_other_players_cards(self):
        pass

    def draw_player_cards(self):
        pass

    def draw_game(self):
        if self.in_game:
            self.draw_dealer_cards()

            self.draw_other_players_cards()

            self.draw_player_cards()

    def bet(self):
        bet_input = self.ui.get_bet_values()
        bet_amount = None

        try:
            bet_amount = int(bet_input)
            msg = {"code": "PLACE_BET", 
                   "response_codes": ["SUCCESS", "FAIL"], 
                   "data": { "username": self.username, 
                             "gamename": self.gamename, 
                             "bet_amount": bet_amount}
                   }
            
            resp = self.send_then_recv(msg)

            if resp["code"] == "SUCCESS":
                self.game_state = resp["data"]["game_state"]
                
            self.ui.set_game_message(resp["data"]["msg"])
            self.ui.set_game_inputs(self.game_state)
            
        except:
            self.ui.set_game_message("That was a bad bet. Try again.")
            self.ui.set_bet_values()

    def play_action(self, action):
        msg = {"code": action, 
                   "response_codes": ["SUCCESS", "FAIL"], 
                   "data": { "username": self.username, 
                             "gamename": self.gamename}
                }
            
        resp = self.send_then_recv(msg)

        if resp["code"] == "SUCCESS":
            self.game_state = resp["data"]["game_state"]

        self.ui.set_game_message(resp["data"]["msg"])
        self.ui.set_game_inputs(self.game_state)
        

    def double_down(self):
        self.play_action("DOUBLE_DOWN")

    def hit(self):
        self.play_action("HIT")

    def stand(self):
        self.play_action("STAND")
    
    def draw_bg(self):
        self.window.blit(self.bg, (0, 0))

    def listen_for_broadcasts(self, timeout):
        for _ in range(timeout):
            try:
                resp = json.loads(self.recv_q.pop(0))

                if resp["code"] == "BROADCAST":
                    if resp["data"]["type"] == "PLAYER_JOIN":
                        #TODO initialize new player and add to players list
                        pass
                    
                    elif resp["data"]["type"] == "PLAYER_LEAVE":
                        #TODO delete player from players list
                        pass

                    elif resp["data"]["type"] == "BET_UPDATE":
                        pass

                    self.ui.set_game_message(resp["data"]["msg"])
                    
                else:
                    self.recv_q.append(json.dumps(resp))
            except:
                pass

    def play(self):
        stop = False
        while not stop:

            self.draw_bg()
            self.draw_game()

            events = pygame.event.get()

            for event in events:

                if event.type == pygame.QUIT:
                    stop = True

                elif event.type == pygame.WINDOWSIZECHANGED:
                    self.bg = pygame.transform.scale(self.bg, self.window.get_size())
                    self.resize_ui()
                
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.ui.switch_to_pause_menu()
            
            self.ui.draw(events)

            self.listen_for_broadcasts(1)
            
            pygame.display.update()

        pygame.quit()
        exit()

    def start(self):
        super().start()
        self.play()
