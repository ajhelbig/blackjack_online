import socket
import threading

port = 5890

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect(("10.0.0.5", port))

def send_msg(sock):
    while True:
        msg = input("> ")
        sock.send(msg.encode())

def recv_msg(sock):
    while True:
        msg = sock.recv(1024)
        print(msg.decode())

threading.Thread(target=send_msg, args=(c,)).start()
threading.Thread(target=recv_msg, args=(c,)).start()

c.close()