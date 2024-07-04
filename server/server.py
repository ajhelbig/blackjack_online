import socket
import threading

class Server:

    def __init__(self, port):
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("server socket created")

        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.s.bind(('',port))
        print("server socket bound to port %s" %(port))

        self.s.listen(5)
        print("server socket is listening")

        self.s.settimeout(1)
        
    def start(self, client_handler):
        try:
            while True:
                try:

                    (client_socket, address) = self.s.accept()

                    print(f"spawning thread to handle client {address}")

                    threading.Thread(target=client_handler, args=(client_socket, address,)).start()
                    
                except socket.timeout:
                    pass

        except KeyboardInterrupt:

            print("\nserver terminated")
            self.s.close()
