from modules.handlers import MsgHandler

class Handler(MsgHandler):
    def name(self):
        return "pref_change"

    def description(self):
        return "設定変更イベントを処理する"
    
    def isPublic(self):
        return False

    def eventType(self):
        return {'type': 'pref_change'}

    def process(self, sc, d):
        #print("pref_change")
        #print(d)
        return False

