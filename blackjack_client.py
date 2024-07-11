from client.client import *

client = Client()
client.connect('10.0.0.5', 5890)
client.start()
