from server.server import Server
import sqlite3
import socket
import select

class DB:

    def __init__(self, port):
        self.con = sqlite3.connect(database='game.db', autocommit=False)
        self.cur = self.con.cursor()

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("server socket created")

        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.s.bind(('', port))
        print("server socket bound to port %s" %(port))

        self.s.listen(5)
        print("server socket is listening")

        self.s.setblocking(False)

        self.chunk_size = 4096

        self.potential_server_readers = [self.s]
        self.potential_server_writers = []

        if self.cur.execute("SELECT name FROM sqlite_master WHERE name='users'").fetchone() is None:
            self.create_users_table()

        if self.cur.execute("SELECT name FROM sqlite_master WHERE name='games'").fetchone() is None:
            self.create_games_table()

    def create_users_table(self):
        self.cur.execute('CREATE TABLE users(name, password, bank, user_id)')

    def create_games_table(self):
        self.cur.execute('CREATE TABLE games(user_id, game data)')

    def send_msg(self, sock, msg):

        msg = msg + '\0'

        totalsent = 0

        while totalsent < len(msg):

            sent = sock.send(msg[totalsent:].encode())

            if sent == 0:
                raise RuntimeError("socket connection broken")

            totalsent = totalsent + sent

    def recv_msg(self, sock):

        chunks = []
        bytes_recd = 0

        while True:

            chunk = sock.recv(self.chunk_size)

            if chunk == b'':
                raise RuntimeError("socket connection broken")

            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)

            if chunk[-1] == 0:
                break

        msg = b''.join(chunks)

        final_msg = msg[:-1]

        return final_msg.decode()

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
