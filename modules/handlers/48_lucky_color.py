import modules.handlers as handlers
import random

class Handler(handlers.MsgHandler):
    def description(self):
        return "「ラッキーカラー」と発言すると適当な色を作成します"
    
    def eventType(self):
        return {'type': 'message', 'subtype': None}

    def isPublic(self):
        return True

    def process(self, sc, data):
        text = data['text']
        ch = data['channel']
        if text != "ラッキーカラー":
            return True
        color = "#"
        for i in range(3):
            color += format(random.randint(0, 255), '02x')
        sc.rtm_send_message(ch, color)
        return False

