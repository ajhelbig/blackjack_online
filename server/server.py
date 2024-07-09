import socket
import select
from client.client import *

class Server:

    def __init__(self, port):
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("server socket created")

        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.s.bind(('', port))
        print("server socket bound to port %s" %(port))

        self.s.listen(5)
        print("server socket is listening")

        self.s.setblocking(False)

        self.potential_server_readers = [self.s]
        self.potential_server_writers = []

        self.num_connections = 0
        self.msg = str()
        self.msg_sent = True

        self.games = dict()

    def handle_new_connection(self, sock):
        client_socket, client_address = sock.s.accept()
        print(f"New connection from {client_address}")
        self.potential_server_readers.append(client_socket)
        self.potential_server_writers.append(client_socket)
        self.num_connections += 1
        print(f"Number of connected clients: {self.num_connections}")

    def handle_existing_connection_read(self, sock):
        try:
            self.msg = sock.recv_msg()
            print(f"Received data from {sock.s.getpeername()}: {self.msg}")
            self.msg_sent = False

        except:# Client disconnected
            print(f"Client {sock.s.getpeername()} disconnected")
            sock.close_connection()
            self.potential_server_readers.remove(sock.s)
            self.potential_server_writers.remove(sock.s)
            self.num_connections -= 1
            print(f"Number of connected clients: {self.num_connections}")

    def handle_ready_to_read(self, ready_to_read):
        for s in ready_to_read:

                    sock = Client(s)# maybe not the best way to go

                    if sock.s is self.s:
                        self.handle_new_connection(sock)

                    else:# Handle data from existing client sockets
                        self.handle_existing_connection_read(sock)

    def handle_ready_to_write(self, ready_to_write):
        if self.num_connections == len(ready_to_write) and not self.msg_sent:

            for s in ready_to_write:

                    sock = Client(s)# maybe not the best way to go
                    
                    sock.send_msg(self.msg)
                    self.msg_sent = True

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
