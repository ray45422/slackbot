import re
from modules.handlers import MsgHandler
import modules.response as response

class Handler(MsgHandler):
    def description(self):
        return "登録された返信メッセージを処理します"
    
    def isPublic(self):
        return True

    def eventType(self):
        return {'type': 'message', 'subtype': None}

    def parseReaction(self, text):
        reactions = []
        if not text.startswith("+"):
            return reactions
        text = re.sub("^\+", "", text)
        text = re.sub("\s+", "", text)
        print("parse reaction" + "-" * 10)
        print(text)
        if re.match("(:[^:]+:)+$", text) is None:
            print("not match")
            return reactions 
        return re.findall(":([^:]+):", text)

    def process(self, sc, data):
        text = data['text']
        channel = data['channel']
        ts = data['ts']
        if text.startswith("responseset "):
            text = text[12:]
            l = text.split('\n')
            n = len(l)
            if n < 2:
                sc.rtm_send_message(channel, '>responseadd pattern\n>response\n[response]\nの形式です')
                return True
            key = l.pop(0)
            value = []
            while len(l) > 0:
                value.append(l.pop(0))
            print(key)
            print(value)
            response.set(key, value)
            sc.rtm_send_message(
                channel, '追加しました')
            return False

        if text == 'responselist':
            s = []
            n = 1
            l = len(str(len(response.list)))
            for p in response.list:
                msg = ("{0:" + str(l) + "d}").format(n) + ". " + str(p)
                s.append(msg)
                n += 1
            sc.rtm_send_message(channel, "\n".join(s))
            return False

        if text.startswith("responsedel "):
            key = text[12:]
            ret = response.remove(key)
            if ret == None:
                sc.rtm_send_message(channel, "失敗しました")
            else:
                sc.rtm_send_message(channel, "\\n".join(ret) + "を削除しました")
            return False

        resp = response.getResponse(text)
        if resp == None:
            return True
        reactions = self.parseReaction(resp)
        print(reactions)
        if len(reactions) == 0:
            sc.rtm_send_message(channel, resp)
        else:
            sc.addReactions(channel, ts, reactions)
        return False
        
