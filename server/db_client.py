from base.client import Client

class DB_Client(Client):

    def __init__(self, s=None):
        super().__init__(s=s)
    
    def sign_in(self, msg):
        self.send_q.append(msg)
        return self.await_msg(msg)
    
    def create_account(self, msg):
        self.send_q.append(msg)
        return self.await_msg(msg)

    def fetch(self, query):
        pass

    def store(self, data):
        pass
