import socket
import threading

def respond_to_client(client_socket):

    client_socket.send(('You connected to the Tic Tac Toe Server!\n').encode())
    client_socket.close()

s = socket.socket()
print("server socket created")

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
            c_thread = threading.Thread(target=respond_to_client, args=(client_socket,))
            c_thread.start()

        except socket.timeout:
            pass

except KeyboardInterrupt:
    print("server terminated")
    s.close()