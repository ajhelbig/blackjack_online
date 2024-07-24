import pygame
import pygame_widgets
import json
from base.client import Client
from client.menus import Menus
from client.input import *

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
        self.players = []
        self.player_hands = []
        self.dealer_hands = []
        self.window_size = (1200, 1000)
        self.set_bg("MENU")

        pygame.init()

        self.window = pygame.display.set_mode(self.window_size, pygame.RESIZABLE)
        self.menus = Menus(self.window,
                           self.sign_in,
                           self.create_account,
                           self.start_game,
                           self.join_game,
                           self.pause_leave_game,
                           self.pause_resume)

        self.play_buttons = get_new_play_buttons(self.window, self.insurance, self.double_down, self.hit, self.stand, self.split, self.surrender)
        self.bet_text_box = get_new_bet_text_box(self.window, self.bet)

    def pause_resume(self):
        self.menus.switch_to_game_message_menu()

    def pause_leave_game(self):
        self.menus.switch_to_main_menu()
        self.leave_game()

    def sign_in(self):
        username, password = self.menus.get_sign_in_values()
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
                self.menus.switch_to_main_menu()

            elif resp["code"] == "BAD_USER":
                display_msg = 'There is no account with that username.\nTry creating an account.'

            elif resp["code"] == "BAD_PSWD":
                display_msg = 'That was not the right password.'

            elif resp["code"] == "DUP_SIGN_IN":
                display_msg = "You are already signed in."
            
        self.menus.set_sign_in_values(display_msg)

    def create_account(self):
        username, password1, password2 = self.menus.get_create_account_values()
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
                self.menus.switch_to_main_menu()

            elif resp["code"] == "USER_TAKEN":
                display_msg = 'That username is already taken.\nTry again.'

        self.menus.set_create_account_values(display_msg)

    def start_game(self):
        gamename, game_password = self.menus.get_start_game_values()
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
                self.menus.switch_to_game_message_menu()
                self.gamename = gamename
                self.in_game = True
                self.game_state = resp["data"]["game_state"]
                self.bank = resp["data"]["starting_bank"]

            elif resp["code"] == "BAD_GAME_NAME":
                display_msg = 'Sorry that game name is already taken.\nTry again'

        self.menus.set_start_game_values(display_msg)

    def join_game(self):
        gamename, game_password = self.menus.get_join_game_values()
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
                self.menus.switch_to_game_message_menu()
                self.gamename = gamename
                self.in_game = True
                self.game_state = resp["data"]["game_state"]
                self.bank = resp["data"]["starting_bank"]

            elif resp["code"] == 'BAD_GAME_NAME':
                display_msg = "That game does not exist.\nTry again."

            elif resp["code"] == 'BAD_GAME_PSWD':
                display_msg = 'That was the wrong password.\nTry again.'

            elif resp["code"] == 'GAME_FULL':
                display_msg = "That game is full."

        self.menus.get_join_game_values(display_msg)

    def leave_game(self):
        msg = {"code": "LEAVE_GAME",
               "response_codes": ["SUCCESS", "FAIL"], 
               "data": { "username": self.username, 
                         "gamename": self.gamename }
                }
        
        resp = self.send_then_recv(msg)

        if resp["code"] == 'SUCCESS':
            self.menus.switch_to_main_menu()
            self.gamename = None
            self.in_game = False
            self.game_state = None
            self.bank = None

            self.active_inputs.hide()
            self.active_inputs = None
            self.bet_text_box = get_new_bet_text_box(self.window, self.bet)

    def send_then_recv(self, json_dict):
        self.send_q.append(json.dumps(json_dict))
        return self.await_msg(json.dumps(json_dict))
    
    def set_bg(self, bg):
        path = None

        if bg == "MENU":
            path = 'assets/images/game_bg.jpg'
        elif bg == "GAME":
            path = 'assets/images/game_bg.jpg'

        self.bg = pygame.image.load(path)
        self.bg = pygame.transform.scale(self.bg, self.window_size)

    def resize_ui(self):
        self.window_size = self.window.get_size()

        self.menus.resize(self.window_size)
        
        self.play_buttons = get_new_play_buttons(self.window, self.insurance, self.double_down, self.hit, self.stand, self.split, self.surrender)
        self.bet_text_box = get_new_bet_text_box(self.window, self.bet)
        
    def draw_dealer_cards(self):
        pass

    def draw_other_players_cards(self):
        pass

    def draw_player_cards(self):
        pass

    def show_inputs(self, button):
        if self.active_inputs is not None:
            self.active_inputs.hide()

        self.active_inputs = button
        self.active_inputs.show()

    def draw_game(self):
        if self.in_game:
            self.draw_dealer_cards()
            self.draw_other_players_cards()
            self.draw_player_cards()

            if self.game_state == "BET":
                self.show_inputs(self.bet_text_box)

            elif self.game_state == "PLAY":
                self.show_inputs(self.play_buttons)
                
            elif self.game_state == "WAITING_FOR_BETS":
                pass

            elif self.game_state == "WAITING_FOR_TURN":
                pass

    def bet(self):
        bet_input = self.bet_text_box.getText()
        bet_amount = None

        try:
            bet_amount = int(bet_input)
            print(bet_amount)
            self.game_state = "PLAY"
            #TODO send bet_amount to server and receive next state
        except:
            self.bet_text_box.placeholderText = "That was a bad bet. Try again."
            self.bet_text_box.setText("")

    def insurance(self):
        print("Insurance")

    def double_down(self):
        print("Double Down")

    def hit(self):
        print("Hit")

    def stand(self):
        print("Stand")

    def split(self):
        print("Split")

    def surrender(self):
        print("Surrender")
    
    def draw_bg(self):
        if self.in_game:
            self.window.blit(self.bg, (0, 120))
        else:
            self.window.blit(self.bg, (0, 0))

    def listen_for_broadcast(self, timeout):
        for _ in range(timeout):
            try:
                resp = json.loads(self.recv_q.pop(0))

                if resp["code"] == "BROADCAST":
                    if resp["data"]["type"] == "PLAYER_JOIN" or \
                       resp["data"]["type"] == "PLAYER_LEAVE":
                        self.menus.set_game_message(resp["data"]["msg"])
                    
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
            pygame_widgets.update(events)

            for event in events:

                if event.type == pygame.QUIT:
                    stop = True

                elif event.type == pygame.WINDOWSIZECHANGED:
                    self.bg = pygame.transform.scale(self.bg, self.window.get_size())
                    self.resize_ui()
                
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.menus.switch_to_pause_menu()
            
            self.menus.draw(events)

            self.listen_for_broadcast(10)
            
            pygame.display.update()

        pygame.quit()
        exit()

    def start(self):
        super().start()
        self.play()
