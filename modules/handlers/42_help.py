import modules.handlers as handlers
import re

class Handler(handlers.MsgHandler):
    def name(self):
        return "help"

    def description(self):
        return "この機能です"
    
    def eventType(self):
        return {'type': 'message', 'subtype': None}

    def isPublic(self):
        return True

    def process(self, sc, data):
        if not sc.isMention(data):
            return True
        text = data['text']
        if "help" not in text:
            return True
        msgs = []
        all = False
        if "all" in text:
            all = True
        keys = sorted(handlers.handlers)
        for key in keys:
            h = handlers.handlers[key]
            if not all and not h.isPublic():
                continue
            msg = str(h.priority()) + " " + h.name() + ": " + h.description()
            msgs.append(msg)
        sc.rtm_send_message(data['channel'], "\n".join(msgs))
        return False

