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

        self.potential_readers = [self.s]
        self.potential_writers = []

        self.num_connections = 0
        self.msg = str()
        self.msg_sent = True

    def start(self):
        while True:
            try:
                ready_to_read, ready_to_write, _ = select.select(
                    self.potential_readers, self.potential_writers, [], 1)

                for s in ready_to_read:
                    sock = Client(s)
                    if sock.s is self.s:# New connection, accept it
                        
                        client_socket, client_address = sock.s.accept()
                        print(f"New connection from {client_address}")
                        self.potential_readers.append(client_socket)
                        self.potential_writers.append(client_socket)
                        self.num_connections += 1

                    else:# Handle data from existing client sockets
                        
                        try:
                            self.msg = sock.recv_msg()
                            print(f"Received data from {sock.getpeername()}: {self.msg}")
                            self.msg_sent = False

                        except:# Client disconnected
                            print(f"Client {sock.s.getpeername()} disconnected")
                            sock.close_connection()
                            self.potential_readers.remove(sock.s)
                            self.potential_writers.remove(sock.s)
                            self.num_connections -= 1

                if self.num_connections == len(ready_to_write) and not self.msg_sent:
                    for sock in ready_to_write:
                            sock.send_msg(self.msg)
                            self.msg_sent = True

            except KeyboardInterrupt:
                print("\nserver terminated")
                for sock in self.potential_readers:
                    sock.close()

                for sock in self.potential_writers:
                    sock.close()

                break
