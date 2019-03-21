import modules.handlers as handlers
import re
import sqlite3
import modules.slack as slack
import modules.datautil as datautil

class Handler(handlers.MsgHandler):
    cmdreg = None
    def __init__(self):
        optlist = [
                r"(?::(?P<emoji>[^:]+):)",
                r"(?:<@(?P<user>\w+)>)",
                r"(?:(?P<fromd>\d{4}/\d{1,2}/\d{1,2})?\s*-\s*(?P<tod>\d{4}/\d{1,2}/\d{1,2})?)",
                r"(?P<date>\d{4}/\d{1,2}/\d{1,2})",
                r"(?P<order>asc|desc)"
            ]
        reg = r"<@\w+>\s*emojistatus(?:\s+(?:" + "|".join(optlist) + "))*"
        self.cmdreg = re.compile(reg)
    def description(self):
        return "絵文字の使用状況を報告します。"
    
    def descriptionDetail(self):
        return """>emojistatus [ranking] [help] [[@user] [[集計開始日]-[集計終了日]] [集計日] [asc|desc]]
ranking: ユーザーごとにランキング形式で表示します。
help: 説明を表示します。
@user: ユーザーへのメンション
日付: スラッシュ"/"区切りの「西暦/月/日」の形式です。
[集計開始日]-[集計終了日]: 指定する場合はどちらか片方が必要です。1日だけ指定する場合は集計日を使用してください。
集計日: 集計する日を指定します。
asc|desc: 昇順の場合"asc"、降順の場合"desc"を指定します。"""

    def eventType(self):
        return {'type': 'message', 'subtype': None}

    def isPublic(self):
        return True

    def ranking(self, sc, data):
        con = sqlite3.connect(datautil.dataDir / "emojiuse.db")
        msgs = []
        query = "select userid, count(*)-(select count(*) from emojiuse B where A.name=B.name and B.del=1) n from emojiuse A where del=0 group by userid order by n desc"
        cur = con.execute(query)
        result = cur.fetchall()
        rank = 0
        for row in result:
            rank += 1
            query = "select count(*)-(select count(*) from emojiuse B where A.name=B.name and B.del=1) n, name from emojiuse A where A.del=0 and A.userid=? group by name order by n desc"
            cur = con.execute(query, [row[0]])
            use = cur.fetchone()
            n = use[0]
            if n < 1:
                continue
            user = sc.getUserByID(row[0])
            msg = str(rank) + "位:"+ user['name'] + " " + str(row[1]) + "回 よく使う絵文字:" + use[1] + ":"
            while True:
                use = cur.fetchone()
                if use is None or use[0] != n:
                    break
                msg += ":" + use[1] + ":"
            msg += str(n) + "回"
            msgs.append(msg)
        sc.rtm_send_message(data['channel'], "\n".join(msgs))
        con.close()
        return False

    def process(self, sc, data):
        if not sc.isMention(data):
            return True
        text = data['text']
        if re.match(r"<@\w+>\s*emojistatus\s+ranking$", text):
            return self.ranking(sc, data)
        mat = self.cmdreg.match(text)
        if mat is None:
            return True
        #print(mat.groupdict())
        wherelist = []
        paramlist = []
        order = "desc"
        d = mat.groupdict()
        if d['emoji'] is not None:
            #絵文字のリストを取得する
            pass
        if d['user'] is not None:
            w = "userid=?"
            wherelist.append(w)
            paramlist.append(d['user'])
        if d['fromd'] is not None or d['tod'] is not None:
            f = d['fromd']
            t = d['tod']
            if f is not None and t is not None:
                w = "date(datetime, 'localtime') between ? and ?"
                wherelist.append(w)
                paramlist.append(f.replace("/", "-"))
                paramlist.append(t.replace("/", "-"))
            elif f is None:
                w = "date(datetime, 'localtime') <= ?"
                wherelist.append(w)
                paramlist.append(t.replace("/", "-"))
            else:
                w = "date(datetime, 'localtime') >= ?"
                wherelist.append(w)
                paramlist.append(f.replace("/", "-"))
        if d['date'] is not None:
            w = "date(datetime, 'localtime') = ?"
            wherelist.append(w)
            paramlist.append(d['date'].replace("/", "-"))
        if d['order'] is not None:
            order = d['order']
        if len(wherelist) != 0:
            where = " and " + " and ".join(wherelist)
        else:
            where = ''
            paramlist = []
        con = sqlite3.connect(datautil.dataDir / "emojiuse.db")
        query = "select date(min(datetime), 'localtime'), date(max(datetime), 'localtime') from emojiuse where del=0" + where
        cur = con.execute(query, paramlist)
        period = cur.fetchone()
        query = "select name, count(*)-(select count(*) from emojiuse B where A.name=B.name and B.del=1) n from emojiuse A where del=0" + where + " group by name having n<>0 order by n " + order
        #print(query)
        #print(paramlist)
        cur = con.execute(query, paramlist)
        msgs = []
        if period is not None:
            msgs.append("集計期間:" + period[0] + "~" + period[1])
        mx = 0
        result = cur.fetchall()
        for row in result:
            if row[1] > mx:
                mx = row[1]
        mx = len(str(mx))
        n = 0
        for row in result:
            if row[1] < 1:
                continue
            if row[1] == n:
                msgs[-1] += ":" + row[0] + ":"
                continue
            n = row[1]
            msg = str(row[1]).zfill(mx) + "回::" + row[0] + ": "
            msgs.append(msg)
        con.close()
        msg = "\n".join(msgs)
        if msg == '':
            msg = "該当するものはありませんでした"
        sc.rtm_send_message(data['channel'], msg)
        return False

