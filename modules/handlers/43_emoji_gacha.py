from modules.handlers import MsgHandler
import re
import modules.slack as slack
from random import randrange

class Handler(MsgHandler):
    count = 20
    def name(self):
        return "emoji_gacha"

    def description(self):
        return "「絵文字(n連)ガチャ」(" + str(self.count) + "≧n≧1)と発言すると、リアクションが付きます"
    
    def eventType(self):
        return {'type': 'message', 'subtype': None}

    def isPublic(self):
        return True

    def process(self, sc, data):
        text = data['text']
        match = re.match("絵文字((?P<count>\d+)連)?ガチャ", text)
        if match is None:
            return True
        d = match.groupdict()
        count = d['count']
        if count is None:
            count = 1
        else:
            count = int(count)
        if count > count or count < 0:
            sc.rtm_send_message(data['channel'], "1～" + count + "の整数にしてください")
            return False
        emoji = sc.getEmoji()
        emojiKey = [*emoji.keys()]
        emojis = {}
        for i in range(count):
            e = emojiKey[randrange(0, len(emojiKey))]
            if e in emojis:
                emojis[e] += 1
            else:
                emojis[e] = 0
        sc.addReactions(data['channel'], data['ts'], [*emojis.keys()])
        msgs = []
        for e in emojis.items():
            if e[1] > 0:
                msg = ":" + e[0] + ":が" + str(e[1]) + "回"
                msgs.append(msg)
        #print(msgs)
        #print(len(msgs))
        if len(msgs) != 0:
            sc.rtm_send_message(data['channel'], "、".join(msgs) + "かぶりました")
        return False

