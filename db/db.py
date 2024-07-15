from server.server import Server
import sqlite3
import socket
import select

class DB(Server):

    def __init__(self, port):

        super().__init__(port=port)

        self.con = sqlite3.connect(database='game.db', autocommit=False)
        self.cur = self.con.cursor()

        if self.cur.execute("SELECT name FROM sqlite_master WHERE name='users'").fetchone() is None:
            self.create_users_table()

        if self.cur.execute("SELECT name FROM sqlite_master WHERE name='games'").fetchone() is None:
            self.create_games_table()

    def create_users_table(self):
        self.cur.execute('CREATE TABLE users(name, password, bank, user_id)')

    def create_games_table(self):
        self.cur.execute('CREATE TABLE games(user_id, game data)')

    def handle_new_connection(self, sock):
        client_socket, _ = sock.accept()
        self.potential_server_readers.append(client_socket)
        self.potential_server_writers.append(client_socket)

    def handle_existing_connection_read(self, sock):
        try:
            msg = self.recv_msg(sock)

            print(f"Received msg: {msg}")

            #handle message

        except:# Client disconnected
            print(f"Client {sock.getpeername()} disconnected")
            sock.close()
            self.potential_server_readers.remove(sock)
            self.potential_server_writers.remove(sock)

    def handle_ready_to_read(self, ready_to_read):
        for sock in ready_to_read:
                    
                    if sock is self.s:
                        self.handle_new_connection(sock)

                    else:
                        self.handle_existing_connection_read(sock)

    def handle_ready_to_write(self, ready_to_write):

        for sock in ready_to_write:
                #process writers
                pass
