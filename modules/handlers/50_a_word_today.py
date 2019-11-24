import re
from modules.handlers import MsgHandler
import modules.db as db

class Handler(MsgHandler):
    tableName = 'A_WORD_TODAY'
    name = "剛体語録"
    addPat = None
    def __init__(self):
        cur = db.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name=?", [self.tableName])
        count = cur.fetchone()[0]
        if count == 0:
            print("table created: " + self.tableName)
            db.execute("CREATE TABLE " + self.tableName + "(insuser, instime, text)")
        self.addPat = re.compile(r"^" + self.name + "追加 ")

    def description(self):
        return self.name + "です"

    def descriptionDetail(self):
        return "登録された" + self.name + """から一つランダムに出力します。
追加方法:
> """ + self.name + """追加 [ここに追加したい文字列]
パターン削除方法:
> hoge
    まだ
パターン一覧:
> huga
    まだ
"""

    def isPublic(self):
        return True

    def eventType(self):
        return {'type': 'message', 'subtype': None}

    def process(self, sc, data):
        text = data['text']
        channel = data['channel']
        ts = data['ts']
        user = data['user']
        if text == self.name:
            cur = db.execute("SELECT text FROM A_WORD_TODAY ORDER BY RANDOM() LIMIT 1")
            result = cur.fetchone()
            if result is None:
                msg = "登録されていません"
            else:
                msg = result[0]
            sc.rtm_send_message(channel, msg)
            return False

        if self.addPat.match(text):
            text = self.addPat.sub("", text)
            param = [user, text]
            db.execute("INSERT INTO A_WORD_TODAY(insuser, instime, text) VALUES(?, CURRENT_DATE, ?)", param)
            sc.rtm_send_message(channel, '追加しました')
            return False

        return True
