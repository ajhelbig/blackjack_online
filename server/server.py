import socket
import select
from server.user import User
from server.db_client import DB_Client

class Server:

    def __init__(self, port, db_host, db_port):

        self.db = DB_Client()
        self.db.connect(host=db_host, port=db_port)

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

        self.num_connections = 0

        self.users = dict()
        self.usernames = dict()
        self.games = dict()

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
        client_socket, client_address = sock.accept()
        print(f"New connection from {client_address}")
        self.potential_server_readers.append(client_socket)
        self.potential_server_writers.append(client_socket)

        new_user = User(client_socket)
        self.users[new_user.id] = new_user

        self.num_connections += 1
        print(f"Number of connected clients: {self.num_connections}")

    def handle_existing_connection_read(self, sock):
        try:
            msg = self.recv_msg(sock).split()

            print(f"Received data from {sock.getpeername()}: {msg}")

            if msg[0] == 'SIGN_IN':

                #interact with database here

                if msg[1] in self.usernames:
                    user = self.users[id(sock)]
                    user.send_q.append("FAIL")
                else:
                    user = self.users[id(sock)]
                    self.usernames[msg[1]] = user
                    user.name = msg[1]
                    user.send_q.append("SUCCESS")

        except:# Client disconnected
            print(f"Client {sock.getpeername()} disconnected")
            sock.close()
            self.potential_server_readers.remove(sock)
            self.potential_server_writers.remove(sock)

            del self.usernames[self.users[id(sock)].name]
            del self.users[id(sock)]

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
                    user = self.users[id(sock)]
                    msg = user.get_next_msg()

                    if not msg:
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
