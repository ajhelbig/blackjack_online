from client.client import *

client = Client()
client.connect('10.0.0.8', 5890)
client.start()
