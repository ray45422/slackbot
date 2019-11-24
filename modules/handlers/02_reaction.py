from modules.handlers import MsgHandler
import modules.datautil as datautil
import modules.slack as slack
import modules.db as db
import sqlite3

class Handler(MsgHandler):
    fileName = datautil.dataDir / 'emojiuse.db'
    tablename = 'emojiuse'
    def __init__(self):
        cur = db.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' and name=?", [self.tablename])
        count = cur.fetchone()[0]
        print(count)
        if count == 0:
            print("newtable created")
            db.execute("CREATE TABLE " + self.tablename + "(name, datetime, userid, del)")

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
        cur = db.execute("SELECT COUNT(*) FROM " + self.tablename + " WHERE name=? AND userid=? GROUP BY del ORDER BY del", [name, user])
        result = cur.fetchall()
        count = 0
        if len(result) >= 2:
            count = result[0][0] - result[1][0]
        elif len(result) > 0:
            count = result[0][0]
        if count <= 0 and delete == 1:
            return False
        cur = db.execute("INSERT INTO " + self.tablename + " VALUES(?,CURRENT_TIMESTAMP,?,?)", [name, user, delete])
        return False

