import re
from modules.handlers import MsgHandler
import modules.response as response

class Handler(MsgHandler):
    def description(self):
        return "登録された返信メッセージを処理します"

    def descriptionDetail(self):
        return """登録されたパターンに対応する返信、もしくはリアクションを行います。
パターン登録変更方法:
> responseset パターン(正規表現)
> 返信
    正規表現については <https://docs.python.org/ja/3.7/library/re.html|ここ> を参照。
    返信は改行するごとにパターンを増やせます。その場合どれが選ばれるかはランダムです。
    すでに同じパターンが存在していた場合は上書きされます。
    返信は「+」から始めて絵文字を書き連ねるとその絵文字でリアクションをつけます。返信してかつリアクションをつけることは現時点ではできません。
パターン削除方法:
> responsedel パターン
    指定したパターンを削除します。
パターン一覧:
> responselist
    これで見ることができますが、あまり見やすくないので <https://slack.ray45422.net/|Web> で確認することをおすすめします。
"""
    
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
        
