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

        if cur.execute("SELECT name FROM sqlite_master WHERE name='games'").fetchone() is None:
            self.create_games_table(cur)

        con.commit()
        con.close()

    def create_users_table(self, cur):
        cur.execute('CREATE TABLE users(name, password, email, bank, user_id, logged_in)')

    def create_games_table(self, cur):
        cur.execute('CREATE TABLE games(user_id, game_id, game data)')

    def handle_new_connection(self, sock):
        client_socket, _ = sock.accept()
        self.potential_server_readers.append(client_socket)
        self.potential_server_writers.append(client_socket)

        new_user = User(client_socket)
        self.db_users[new_user.id] = new_user

        self.num_connections += 1
        print(f"Number of connected clients: {self.num_connections}")

    def handle_sign_in(self, sock, msg):
        con = sqlite3.connect(database=self.db_name, autocommit=self.db_autocommit)
        cur = con.cursor()
        user = self.db_users[id(sock)]

        query = "SELECT name FROM users WHERE name = ?"
        res = cur.execute(query, (msg[-2], ))

        if res.fetchone() is None:
            user.send_q.append(msg[3])
            con.commit()
            con.close()
            return
        
        query = "SELECT name FROM users WHERE name = ? AND password = ?"
        res = cur.execute(query, (msg[-2], msg[-1]))

        if res.fetchone() is None:
            user.send_q.append(msg[4])
            con.commit()
            con.close()
            return
        
        user.send_q.append(msg[2])
        con.commit()
        con.close()

    def handle_create_account(self, sock, msg):
        con = sqlite3.connect(database=self.db_name, autocommit=self.db_autocommit)
        cur = con.cursor()
        user = self.db_users[id(sock)]

        query = "SELECT name FROM users WHERE name = ?"
        res = cur.execute(query, (msg[-3], ))

        if res.fetchone() is not None:
            user.send_q.append(msg[3])
            con.commit()
            con.close()
            return
        
        query = "SELECT COUNT(*) FROM users"
        cur.execute(query)
        res = cur.fetchone()
        num_users = int(res[0])

        data = msg[-3:]
        data.append(0)
        data.append(num_users + 1)
        data.append(True)
        data = tuple(data)
        
        query = "INSERT INTO users(name, password, email, bank, user_id, logged_in) VALUES (?, ?, ?, ?, ?, ?)"
        res = cur.execute(query, data)
        
        user.send_q.append(msg[2])
        con.commit()
        con.close()

    def handle_existing_connection_read(self, sock):
        try:
            msg = self.recv_msg(sock).split()
            print(f"Received msg: {msg}")

            if msg[0] == 'SIGN_IN':
                self.handle_sign_in(sock, msg)

            elif msg[0] == 'CREATE_ACCOUNT':
                self.handle_create_account(sock, msg)

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

                    if not msg:
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
