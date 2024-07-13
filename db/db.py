import sqlite3

class DB:

    def __init__(self):
        self.con = sqlite3.connect('user.db')
        self.cur = self.con.cursor()
        self.cur.execute('CREATE TABLE user(name, bank)')

db = DB()
res = db.cur.execute('SELECT name FROM sqlite_master')
res.fetchone()