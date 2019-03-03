import modules.handlers as handlers
import re
import random

class Handler(handlers.MsgHandler):
    def description(self):
        return "サイコロを振ります"
    
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

