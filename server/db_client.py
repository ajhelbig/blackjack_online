import socket
from client.client import Client

class DB_Client(Client):

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("db socket created")

    def fetch(self, query):
        pass

    def store(self, data):
        pass
