from client.game_client import Game_Client

client = Game_Client()
client.connect('10.0.0.14', 5890)
client.start()
