import modules.handlers as handlers
import re
import subprocess

class Handler(handlers.MsgHandler):
    min = 4000
    max = 2 ** 256 + 1
    def description(self):
        return "数字が素数か判定します"
    
    def eventType(self):
        return {'type': 'message', 'subtype': None}

    def isPublic(self):
        return True

    last = {}
    url = re.compile("http(s)?://([\w\-]+\.)+[\w\-]+([\w\-./?%&=]*)?")
    def process(self, sc, data):
        text = self.url.sub("", data['text'])
        print(text)
        ch = data['channel']
        isAsk = "isprime" in text
        li = re.findall("\d+", text)
        l = []
        skips = []
        msgs = []
        for i in range(len(li)):
            nStr = li.pop(0)
            n = int(nStr)
            if not isAsk and n < self.min:
                continue
            if n > self.max:
                skips.append(nStr)
            else:
                l.append(nStr)
        if len(l) == 0:
            if isAsk and len(skips) != 0:
                msg = "と".join(skips) + "は大きいのでスキップしました"
                msgs.append(msg)
                sc.rtm_send_message(ch, msg)
            return True
        l = ["factor"] + l
        result = subprocess.run(l, capture_output = True)
        out = result.stdout.decode('utf-8').split('\n')
        primes = []
        for l in out:
            arr = l.split(' ')
            if len(arr) == 1:
                continue
            org = int(arr.pop(0).replace(':', ''))
            isPrime = len(arr) == 1
            if isPrime:
                org = str(org)
                if org not in primes:
                    primes.append(str(org))
                continue
            if not isAsk:
                continue
            msg = []
            for n in arr:
                msg.append(str(n))
            msg = str(org) + "は" + "×".join(msg) + "です"
            msgs.append(msg)
        if isAsk and len(skips) != 0:
            msgs = ["と".join(skips) + "は大きいのでスキップしました"] + msgs
        if len(primes) != 0:
            msgs = ["と".join(primes) + "は素数です。"] + msgs
        print(msgs)
        if len(msgs) != 0:
            sc.rtm_send_message(ch, "\n".join(msgs))
        return True

