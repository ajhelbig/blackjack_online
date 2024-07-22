from base.server import Server
from base.user import User
import sqlite3
import select
import json

class DB(Server):

    def __init__(self, port):
        super().__init__(port=port)

        self.db_sockets = dict()

        self.num_connections = 0
        self.db_name = 'game.db'

        con = sqlite3.connect(database=self.db_name, )
        cur = con.cursor()

        if cur.execute("SELECT name FROM sqlite_master WHERE name='users'").fetchone() is None:
            self.create_users_table(cur)

        con.commit()
        con.close()

    def create_users_table(self, cur):
        cur.execute('CREATE TABLE users(username, password)')

    def handle_new_connection(self, sock):
        client_socket, _ = sock.accept()
        self.potential_server_readers.append(client_socket)
        self.potential_server_writers.append(client_socket)

        new_user = User(client_socket)
        self.db_sockets[new_user.id] = new_user

        self.num_connections += 1
        print(f"Number of connected clients: {self.num_connections}")

    def sign_in(self, sock, msg):
        con = sqlite3.connect(database=self.db_name)
        cur = con.cursor()
        user = self.db_sockets[id(sock)]

        success = msg["response_codes"][0]
        bad_username = msg["response_codes"][1]
        bad_password = msg["response_codes"][2]
        username = msg["data"]["username"]
        password = msg["data"]["password"]

        ret_msg = {"code": None}

        query = "SELECT username FROM users WHERE username = ?"
        res = cur.execute(query, (username, ))

        if res.fetchone() is None:
            ret_msg["code"] = bad_username
            user.send_q.append(json.dumps(ret_msg))
            con.commit()
            con.close()
            return
        
        query = "SELECT username FROM users WHERE username = ? AND password = ?"
        res = cur.execute(query, (username, password))

        if res.fetchone() is None:
            ret_msg["code"] = bad_password
            user.send_q.append(json.dumps(ret_msg))
            con.commit()
            con.close()
            return
        
        ret_msg["code"] = success
        user.send_q.append(json.dumps(ret_msg))
        
        con.commit()
        con.close()

    def create_account(self, sock, msg):
        con = sqlite3.connect(database=self.db_name)
        cur = con.cursor()
        user = self.db_sockets[id(sock)]
        
        success = msg["response_codes"][0]
        username_taken = msg["response_codes"][1]
        username = msg["data"]["username"]
        password = msg["data"]["password"]

        ret_msg = {"code": None}

        query = "SELECT username FROM users WHERE username = ?"
        res = cur.execute(query, (username, ))

        if res.fetchone() is not None:
            ret_msg["code"] = username_taken
            user.send_q.append(json.dumps(ret_msg))
            con.commit()
            con.close()
            return

        username_and_password = [username, password]
        username_and_password = tuple(username_and_password)
        
        query = "INSERT INTO users(username, password) VALUES (?, ?)"
        res = cur.execute(query, username_and_password)
        
        ret_msg["code"] = success
        user.send_q.append(json.dumps(ret_msg))
        con.commit()
        con.close()

    def handle_existing_connection_read(self, sock):
        try:
            msg = json.loads(self.recv_msg(sock))

            if msg["code"] == 'SIGN_IN':
                self.sign_in(sock, msg)

            elif msg["code"] == 'CREATE_ACCOUNT':
                self.create_account(sock, msg)

        except Exception as e:
            print(e)
            print(f"Client {sock.getpeername()} disconnected")
            sock.close()
            self.potential_server_readers.remove(sock)
            self.potential_server_writers.remove(sock)

            del self.db_sockets[id(sock)]

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
                    user = self.db_sockets[id(sock)]
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
