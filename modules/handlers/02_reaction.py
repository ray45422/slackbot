from modules.handlers import MsgHandler
import modules.datautil as datautil
import modules.slack as slack
import sqlite3

class Handler(MsgHandler):
    fileName = datautil.basedir / 'data/emojiuse.db'
    tablename = 'emojiuse'
    con = None
    def __init__(self):
        self.con = sqlite3.connect(self.fileName)
        cur = self.con.cursor()
        cur.execute("select count(*) from sqlite_master where type='table' and name=?", [self.tablename])
        count = cur.fetchone()[0]
        print(count)
        if count == 0:
            print("newtable created")
            cur.execute("create table " + self.tablename + "(name, datetime, userid, del)")
            self.con.commit()
    def __del__(self):
        self.con.commit()
        self.con.close()

    def description(self):
        return "リアクションイベントを処理する"
    
    def isPublic(self):
        return False

    def eventType(self):
        return {'type': 'reaction_(added|removed)'}
    
    def process(self, sc, d):
        print("reaction")
        t = d['type']
        name = d['reaction']
        user = d['user']
        if slack.getClient().myID == user:
            #print("bot reaction")
            return False
        delete = 0
        if t == 'reaction_removed':
            delete = 1
        cur = self.con.cursor()
        cur.execute("insert into " + self.tablename + " values(?,CURRENT_TIMESTAMP,?,?)", (name, user, delete))
        self.con.commit()
        return False

