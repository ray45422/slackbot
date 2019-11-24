import modules.handlers as handlers
import sqlite3
import re
import modules.slack as slack
import modules.datautil as datautil
import modules.db as db

class Handler(handlers.MsgHandler):
    def description(self):
        return "データベースにアクセスします"

    def eventType(self):
        return {'type': 'message', 'subtype': None}

    def isPublic(self):
        return True

    def process(self, sc, data):
        text = data['text']
        match = re.match(r"^query (.+)", text)
        if match is None:
            return True
        query = match.group(1)
        if re.match(r"^select ", query.lower()) is None:
            sc.rtm_send_message(data['channel'], "SELECTのみ許可されています")
            return False
        try:
            cur = db.execute(query)
        except sqlite3.OperationalError as e:
            sc.rtm_send_message(data['channel'], str(e))
            return False
        result = cur.fetchall()
        msgs = []
        msg = []
        for des in cur.description:
            msg.append(des[0])
        msgs.append("\t".join(msg))
        msg = ''
        for row in result:
            row = [str(e) for e in row]
            msg = "\t".join(row)
            msgs.append(str(msg))
        msg = "\n".join(msgs)
        if len(result) == 0:
            msg = "選択されませんでした"
        sc.rtm_send_message(data['channel'], msg)
        return False

