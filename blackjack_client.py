from client.client import *

c = Client()
c.connect('127.0.0.1', 5890)
c.start()
c.close_connection()
