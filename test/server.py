import socket
import select
import random
import time

port = 5890
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Server socket created")

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind(('', port))
print(f"Server socket bound to port {port}")

s.listen(5)
print("Server socket is listening")

s.setblocking(False)

# Initialize lists for monitoring
potential_readers = [s]  # Add the server socket to the list
potential_writers = []

msg_num = 1

while True:
    try:
        ready_to_read, ready_to_write, _ = select.select(
            potential_readers, potential_writers, [], 1)

        for sock in ready_to_read:
            if sock is s:# New connection, accept it
                
                client_socket, client_address = s.accept()
                print(f"New connection from {client_address}")
                state = "GETUSERNAME"
                potential_readers.append(client_socket)
                potential_writers.append(client_socket)

            else:# Handle data from existing client sockets
                
                data = sock.recv(1024)

                if data:
                    print(f"Received data from {sock.getpeername()}: {data.decode()}")
                else:
                    # Client disconnected
                    print(f"Client {sock.getpeername()} disconnected")
                    sock.close()
                    potential_readers.remove(sock)
                    potential_writers.remove(sock)
                    

        for sock in ready_to_write:
                if state == "GETUSERNAME":
                    response = f"message #{msg_num}"
                    sock.send(response.encode())
                    msg_num += 1
                    time.sleep(random.randrange(1, 5))

    except KeyboardInterrupt:
        print("\nServer terminated")
        for sock in potential_readers:
            sock.close()

        for sock in potential_writers:
            sock.close()

        break
          

