from server.server import Server

server = Server(port=5890)
server.connect(host='10.0.0.8', port=5891)
server.start()
