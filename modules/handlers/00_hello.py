from modules.handlers import MsgHandler

class Handler(MsgHandler):
    def name(self):
        return "hello"

    def description(self):
        return "接続メッセージとかを処理する"
    
    def isPublic(self):
        return False

    def eventType(self):
        return {'type': 'hello'}

    def process(self, sc, data):
        print("connected")
        return False

