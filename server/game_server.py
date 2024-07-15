import select
from base.server import Server
from server.user import User
from server.db_client import DB_Client

class Game_Server(Server):

    def __init__(self, port, db_host, db_port):

        super().__init__(port=port)

        self.db = DB_Client()
        self.db.connect(host=db_host, port=db_port)
        self.db.start()

        self.num_connections = 0

        self.server_users = dict()
        self.usernames = dict()
        self.games = dict()

    def handle_new_connection(self, sock):
        client_socket, client_address = sock.accept()
        print(f"New connection from {client_address}")
        self.potential_server_readers.append(client_socket)
        self.potential_server_writers.append(client_socket)

        new_user = User(client_socket)
        self.server_users[new_user.id] = new_user

        self.num_connections += 1
        print(f"Number of connected clients: {self.num_connections}")

    def handle_sign_in(self, sock, msg):
        user = self.server_users[id(sock)]
        ret_val = self.db.sign_in(msg=' '.join(msg))
        user.send_q.append(ret_val)

        if ret_val == 'SUCCESS':
            self.usernames[msg[1]] = user
            user.name = msg[1]

    def handle_create_account(self, sock, msg):
        user = self.server_users[id(sock)]
        ret_val = self.db.create_account(msg=' '.join(msg))
        user.send_q.append(ret_val)

        if ret_val == 'SUCCESS':
            self.usernames[msg[1]] = user
            user.name = msg[1]

    def handle_existing_connection_read(self, sock):
        try:
            msg = super().recv_msg(sock).split()
            print(f"Received data from {sock.getpeername()}: {msg}")

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

            del self.usernames[self.server_users[id(sock)].name]
            del self.server_users[id(sock)]

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
                    user = self.server_users[id(sock)]
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
                print("\nserver terminated")
                for sock in self.potential_server_readers:
                    sock.close()

                for sock in self.potential_server_writers:
                    sock.close()

                break
