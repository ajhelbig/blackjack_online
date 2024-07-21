from server.game_server import Game_Server

server = Game_Server(port=5890, db_host='10.0.0.5', db_port=5891)
server.start()
