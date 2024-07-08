import socket
import select

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

num_connections = 0
msg = str()
msg_sent = True

while True:
    try:
        ready_to_read, ready_to_write, _ = select.select(
            potential_readers, potential_writers, [], 5)

        for sock in ready_to_read:
            if sock is s:# New connection, accept it
                
                client_socket, client_address = s.accept()
                print(f"New connection from {client_address}")
                potential_readers.append(client_socket)
                potential_writers.append(client_socket)
                num_connections += 1

            else:# Handle data from existing client sockets
                
                data = sock.recv(1024)

                if data:
                    print(f"Received data from {sock.getpeername()}: {data.decode()}")
                    msg = data.decode()
                    msg_sent = False

                else:
                    # Client disconnected
                    print(f"Client {sock.getpeername()} disconnected")
                    sock.close()
                    potential_readers.remove(sock)
                    potential_writers.remove(sock)
                    num_connections -= 1
                    
        if num_connections == len(ready_to_write) and not msg_sent:
            for sock in ready_to_write:
                    response = f"{msg}"
                    sock.send(response.encode())
                    msg_sent = True

    except KeyboardInterrupt:
        print("\nserver terminated")
        for sock in potential_readers:
            sock.close()

        for sock in potential_writers:
            sock.close()

        break
          

