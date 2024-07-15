from server.server import Server

server = Server(port=5890, db_host='10.0.0.8', db_port=5891)
server.start()
