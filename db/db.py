from base.server import Server
from base.user import User
import sqlite3
import select

class DB(Server):

    def __init__(self, port):
        super().__init__(port=port)

        self.db_users = dict()

        self.num_connections = 0
        self.db_name = 'game.db'
        self.db_autocommit = False

        con = sqlite3.connect(database=self.db_name, autocommit=self.db_autocommit)
        cur = con.cursor()

        if cur.execute("SELECT name FROM sqlite_master WHERE name='users'").fetchone() is None:
            self.create_users_table(cur)

        if cur.execute("SELECT name FROM sqlite_master WHERE name='blackjack_games'").fetchone() is None:
            self.create_games_table(cur)

        con.commit()
        con.close()

    def create_users_table(self, cur):
        cur.execute('CREATE TABLE users(username, password, email, bank)')

    def create_games_table(self, cur):
        cur.execute('CREATE TABLE blackjack_games(username, gamename, game_password, num_players, current_level, house_bank, deck)')

    def handle_new_connection(self, sock):
        client_socket, _ = sock.accept()
        self.potential_server_readers.append(client_socket)
        self.potential_server_writers.append(client_socket)

        new_user = User(client_socket)
        self.db_users[new_user.id] = new_user

        self.num_connections += 1
        print(f"Number of connected clients: {self.num_connections}")

    def sign_in(self, sock, msg):
        con = sqlite3.connect(database=self.db_name, autocommit=self.db_autocommit)
        cur = con.cursor()
        user = self.db_users[id(sock)]

        query = "SELECT username FROM users WHERE username = ?"
        res = cur.execute(query, (msg[5], ))

        if res.fetchone() is None:
            user.send_q.append(msg[3])
            con.commit()
            con.close()
            return
        
        query = "SELECT username FROM users WHERE username = ? AND password = ?"
        res = cur.execute(query, (msg[5], msg[6]))

        if res.fetchone() is None:
            user.send_q.append(msg[4])
            con.commit()
            con.close()
            return
        
        query = "SELECT bank FROM users WHERE username = ?"
        res = cur.execute(query, (msg[5], ))

        resp_msg = msg[2] + ' ' + res.fetchone()[0]
        
        user.send_q.append(resp_msg)
        con.commit()
        con.close()

    def create_account(self, sock, msg):
        con = sqlite3.connect(database=self.db_name, autocommit=self.db_autocommit)
        cur = con.cursor()
        user = self.db_users[id(sock)]

        query = "SELECT username FROM users WHERE username = ?"
        res = cur.execute(query, (msg[4], ))

        if res.fetchone() is not None:
            user.send_q.append(msg[3])
            con.commit()
            con.close()
            return

        data = msg[4:]
        data.append("0")
        data = tuple(data)
        
        query = "INSERT INTO users(username, password, email, bank) VALUES (?, ?, ?, ?)"
        res = cur.execute(query, data)

        resp_msg = msg[2] + " " + data[3]
        
        user.send_q.append(resp_msg)
        con.commit()
        con.close()

    def start_game(self, sock, msg, type):
        con = sqlite3.connect(database=self.db_name, autocommit=self.db_autocommit)
        cur = con.cursor()
        user = self.db_users[id(sock)]

        if type == 0:
            query = "SELECT gamename FROM blackjack_games WHERE gamename = ?"
            res = cur.execute(query, (msg[5], ))

            if res.fetchone() is not None:
                user.send_q.append(msg[3])
                con.commit()
                con.close()
                return

            data = msg[4:]
            data.append("1")
            data.append("1")
            data = tuple(data)
            
            query = "INSERT INTO blackjack_games(username, gamename, game_password, num_players, current_level) VALUES (?, ?, ?, ?, ?)"
            res = cur.execute(query, data)
            
            user.send_q.append(msg[2])
            con.commit()
            con.close()

    def join_game(self, sock, msg, type):
        con = sqlite3.connect(database=self.db_name, autocommit=self.db_autocommit)
        cur = con.cursor()
        user = self.db_users[id(sock)]

        if type == 0:
            query = "SELECT game_password FROM blackjack_games WHERE gamename = ?"
            res = cur.execute(query, (msg[7], ))
            password = res.fetchone()

            if password is None:
                    user.send_q.append(msg[3])
                    con.commit()
                    con.close()
                    return

            password = password[0]

            if password != "NULL" and password != msg[8]:
                    user.send_q.append(msg[4])
                    con.commit()
                    con.close()
                    return

            query = "SELECT num_players FROM blackjack_games WHERE gamename = ?"
            res = cur.execute(query, (msg[7], ))

            new_num_players = int(res.fetchone()[0]) + 1

            print(new_num_players)

            if new_num_players > 7:
                user.send_q.append(msg[5])
                con.commit()
                con.close()
                return
            
            query = "INSERT INTO blackjack_games(num_players) VALUES (?)"
            res = cur.execute(query, str(new_num_players))
            
            #TODO return house bank and current level
            user.send_q.append(msg[2])
            con.commit()
            con.close()

    def leave_game(self, sock, msg, type):
        #TODO decrement num_players update house bank if last player to leave
        pass

    def handle_existing_connection_read(self, sock):
        try:
            msg = self.recv_msg(sock).split()
            print(f"Received msg: {msg}")

            if msg[0] == 'SIGN_IN':
                self.sign_in(sock, msg)

            elif msg[0] == 'CREATE_ACCOUNT':
                self.create_account(sock, msg)

            elif msg[0] == 'START_GAME_TYPE_0':
                self.start_game(sock, msg, 0)

            elif msg[0] == 'JOIN_GAME_TYPE_0':
                self.join_game(sock, msg, 0)

            elif msg[0] == 'LEAVE_GAME_TYPE_0':
                self.leave_game(sock, msg, 0)

        except Exception as e:
            print(e)
            print(f"Client {sock.getpeername()} disconnected")
            sock.close()
            self.potential_server_readers.remove(sock)
            self.potential_server_writers.remove(sock)

            del self.db_users[id(sock)]

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
                    user = self.db_users[id(sock)]
                    msg = user.get_next_msg()

                    if msg is None:
                        pass
                    else:
                        super().send_msg(sock, msg)
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
                print("\ndb terminated")
                for sock in self.potential_server_readers:
                    sock.close()

                for sock in self.potential_server_writers:
                    sock.close()

                break
