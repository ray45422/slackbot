import modules.handlers as handlers
import re
import random

class Handler(handlers.MsgHandler):
    def description(self):
        return "サイコロを振ります。使用方法は「(回数)D(出目の数)」(各数字は1以上の整数)(かっこは不要)です"

    def descriptionDetail(self):
        return """出目の数と回数を指定してサイコロをシミュレートします。
例えば「1D6」と発言すると6面ダイス(出目は1~6)を1回振った結果を返します。
複数回を指定した場合は合計と、文字数が長すぎない場合に内訳を表示します。
"""
    
    def eventType(self):
        return {'type': 'message', 'subtype': None}

    def isPublic(self):
        return True

    def process(self, sc, data):
        text = data['text']
        m = re.match("(?P<count>\d+)[dD](?P<suf>\d+)$", text)
        if m is None:
            return True
        d = m.groupdict()
        c = int(d['count'])
        s = int(d['suf'])
        if c < 1 or s < 1:
            return True
        sum = 0
        t = []
        for i in range(c):
            v = random.randint(1, s)
            t.append(str(v))
            sum += v
        msg = str(sum)
        deme = "(" + ",".join(t) + ")"
        if len(deme) < 150:
            msg += deme
        #msg += str(len(deme))
        sc.rtm_send_message(data['channel'], msg)
        return False

