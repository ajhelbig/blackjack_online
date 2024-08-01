import select
import json
from base.server import Server
from base.user import User
from server.db_client import DB_Client
from blackjack.game import Game

class Game_Server(Server):

    def __init__(self, port, db_host, db_port):

        super().__init__(port=port)

        self.db = DB_Client()
        self.db.connect(host=db_host, port=db_port)
        self.db.start()

        self.num_connections = 0

        self.server_sockets = dict()
        self.users = dict()
        self.active_games = dict()

    def handle_new_connection(self, sock):
        client_socket, client_address = sock.accept()
        print(f"New connection from {client_address}")
        self.potential_server_readers.append(client_socket)
        self.potential_server_writers.append(client_socket)

        new_user = User(client_socket)
        self.server_sockets[new_user.id] = new_user

        self.num_connections += 1
        print(f"Number of connected clients: {self.num_connections}")

    def sign_in(self, sock,  msg):
        user = self.server_sockets[id(sock)]
        username = msg["data"]["username"]
        dup_sign_in = msg["response_codes"][3]

        ret_msg = {"code": None}

        if username in self.users:
            ret_msg["code"] = dup_sign_in
            user.send_q.append(json.dumps(ret_msg))
            return
        
        ret_val = self.db.send(json.dumps(msg))
        user.send_q.append(json.dumps(ret_val))

        if ret_val["code"] == 'SUCCESS':
            self.users[username] = user
            user.name = username

    def create_account(self, sock, msg):
        user = self.server_sockets[id(sock)]
        ret_val = self.db.send(json.dumps(msg))
        user.send_q.append(json.dumps(ret_val))

        if ret_val["code"] == 'SUCCESS':
            username = msg["data"]["username"]

            self.users[username] = user
            user.name = username

    def start_game(self, msg):
        user = self.users[msg["data"]["username"]]
        
        gamename = msg["data"]["gamename"]
        game_password = msg["data"]["game_password"]
        success = msg["response_codes"][0]
        bad_game_name = msg["response_codes"][1]

        ret_msg = {"code": None, "data": {"game_state": None, "starting_bank": None}}

        if gamename in self.active_games:
            ret_msg["code"] = bad_game_name
        else:
            new_game = Game(gamename, game_password)
            new_game.add_player(user.name)
            self.active_games[gamename] = new_game
            user.add_game(new_game)

            ret_msg["code"] = success
            ret_msg["data"]["game_state"] = new_game.state
            ret_msg["data"]["starting_bank"] = new_game.player_starting_bank

        user.send_q.append(json.dumps(ret_msg))

    def join_game(self, msg):
        username = msg["data"]["username"]
        user = self.users[username]
        
        success = msg["response_codes"][0]
        bad_game_name = msg["response_codes"][1]
        bad_game_password = msg["response_codes"][2]
        game_full = msg["response_codes"][3]
        gamename = msg["data"]["gamename"]
        game_password = msg["data"]["game_password"]

        ret_msg = {"code": None, "data": {"game_state": None}}

        game = None

        if gamename not in self.active_games:
            ret_msg["code"] = bad_game_name
            user.send_q.append(json.dumps(ret_msg))
            return
        else:
            game = self.active_games[gamename]

        if not game.good_password(game_password):
            ret_msg["code"] = bad_game_password
            
        elif not game.add_player(user.name):
            ret_msg["code"] = game_full
        
        else:
            user.add_game(game)
            ret_msg["code"] = success
            ret_msg["data"]["game_state"] = game.state
            ret_msg["data"]["starting_bank"] = game.player_starting_bank

            broadcast_msg = {"code": "BROADCAST", 
                         "data": {"type": "PLAYER_JOIN", 
                                  "msg": f"{username} joined the game!"}}

            user.broadcast(self.users, broadcast_msg)

        user.send_q.append(json.dumps(ret_msg))
        
    def leave_game(self, msg):
        ret_msg = {"code": None}
        success = msg["response_codes"][0]
        fail = msg["response_codes"][1]

        try:
            username = msg["data"]["username"]
            user = self.users[username]

            broadcast_msg = {"code": "BROADCAST", 
                         "data": {"type": "PLAYER_LEAVE", 
                                  "msg": f"{username} left the game."}}
            
            user.broadcast(self.users, broadcast_msg)
            
            self.remove_user_from_game(user)
            ret_msg["code"] = success

        except:
            ret_msg["code"] = fail
            
        user.send_q.append(json.dumps(ret_msg))

    def remove_user_from_game(self, user):
        game = self.active_games[user.game.name]
        game.remove_player(user.name)
        user.remove_game()

        if game.num_players == 0:
            del self.active_games[game.name]

    def game_action(self, msg):
        code = msg["code"]
        username = msg["data"]["username"]
        user = self.users[username]
        gamename = msg["data"]["gamename"]
        game = self.active_games[gamename]

        if code == "PLACE_BET":
            bet_amount = msg["data"]["bet_amount"]
            ret_msg = game.place_bet(username, bet_amount)
        
        elif code == "HIT":
            ret_msg = game.hit(username)

        elif code == "STAND":
            ret_msg = game.stand(username)

        elif code == "DOUBLE_DOWN":
            ret_msg = game.double_down(username)

        user.send_q.append(json.dumps(ret_msg))
          
    def handle_existing_connection_read(self, sock):
        try:
            msg = json.loads(self.recv_msg(sock))

            if msg["code"] == 'SIGN_IN':
                self.sign_in(sock, msg)

            elif msg["code"] == 'CREATE_ACCOUNT':
                self.create_account(sock, msg)

            elif msg["code"] == 'START_GAME':
                self.start_game(msg)
            
            elif msg["code"] == 'JOIN_GAME':
                self.join_game(msg)

            elif msg["code"] == 'LEAVE_GAME':
                self.leave_game(msg)
            
            elif msg["code"] == 'PLACE_BET' or \
                 msg["code"] == 'HIT' or \
                 msg["code"] == 'STAND' or \
                 msg["code"] == 'DOUBLE_DOWN':
                self.game_action(msg)

        except Exception as e:
            print(f"error: {e}")
            print(f"Client {sock.getpeername()} disconnected")
            sock.close()
            self.potential_server_readers.remove(sock)
            self.potential_server_writers.remove(sock)
            user = self.server_sockets[id(sock)]
            
            if user.in_game:
                broadcast_msg = {"code": "BROADCAST", 
                         "data": {"type": "PLAYER_LEAVE", 
                                  "msg": f"{user.name} left the game."}}
                
                user.broadcast(self.users, broadcast_msg)

                self.remove_user_from_game(user)

            if user.name is not None:
                del self.users[user.name]

            del self.server_sockets[id(sock)]

            self.num_connections -= 1
            print(f"Number of connected clients: {self.num_connections}")

    def handle_ready_to_read(self, ready_to_read):
        for sock in ready_to_read:
                    
                    if sock is self.s:
                        self.handle_new_connection(sock)

                    else:
                        self.handle_existing_connection_read(sock)

    def handle_ready_to_write(self, ready_to_write):

        for sock in ready_to_write:
                try:
                    user = self.server_sockets[id(sock)]
                    msg = user.get_next_msg()

                    if msg is None:
                        pass
                    else:
                        self.send_msg(sock, msg)
                except:
                    pass

    def start(self):
        while True:
            try:
                ready_to_read, ready_to_write, _ = select.select(
                    self.potential_server_readers, self.potential_server_writers, [], 1)

                self.handle_ready_to_read(ready_to_read)

                self.handle_ready_to_write(ready_to_write)

            except KeyboardInterrupt:
                print("\nserver terminated")
                for sock in self.potential_server_readers:
                    sock.close()

                for sock in self.potential_server_writers:
                    sock.close()

                break
        
        exit()
