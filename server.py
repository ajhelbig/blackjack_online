import socket
import threading
from client import *

games = dict()

def respond_to_client(client_socket, address):

    c = ClientSocket(client_socket)

    msg = c.c_recv()

    if msg == "start game\0":
        c.c_send("starting game\0")
        #create a new game

    c.c_close()

s = socket.socket()
print("server socket created")

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

port = 5890

s.bind(('',port))
print("server socket bound to port %s" %(port))

s.listen(5)
print("server socket is listening")

s.settimeout(1)

try:
    while True:
        try:

            (client_socket, address) = s.accept()

            print(f"spawning thread to handle client with address:\n{address}")

            c_thread = threading.Thread(target=respond_to_client, args=(client_socket, address,))
            c_thread.start()

        except socket.timeout:
            pass

except KeyboardInterrupt:

    print("\nserver terminated")
    s.close()
