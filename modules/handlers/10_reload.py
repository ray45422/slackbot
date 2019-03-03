import modules.handlers as handlers
from modules.handlers import MsgHandler

class Handler(MsgHandler):
    def name(self):
        return "reload"

    def description(self):
        return "モジュールを再読込します"
    
    def eventType(self):
        return {'type': 'message', 'subtype': None}

    def isPublic(self):
        return False

    def process(self, sc, data):
        if data['text'] != 'reload':
            return True
        handlers._reload()
        sc.rtm_send_message(data['channel'], 'リロードしました')
        return False


