from modules.handlers import MsgHandler
import re

class Handler(MsgHandler):
    def name(self):
        return "eval"

    def description(self):
        return "evalです"
    
    def eventType(self):
        return {'type': 'message', 'subtype': None}

    def isPublic(self):
        return True

    def process(self, sc, data):
        text = data['text']
        channel = data['channel']
        if text.startswith("eval ") and data['user'] == "U06J4VD8X":
            cmd = text[5:]
            try:
                t = str(eval(cmd))
                sc.rtm_send_message(channel, t)
            except Exception as e:
                t = 'Exception: ' + str(e.args)
                sc.rtm_send_message(channel, t)
            return False
        return True

