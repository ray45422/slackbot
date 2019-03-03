from modules.handlers import MsgHandler

class Handler(MsgHandler):
    def name(self):
        return "leftevent"

    def description(self):
        return "誰にも処理されなかったイベントの辿り着く場所"
    
    def eventType(self):
        return {}

    def process(self, sc, data):
        print("最後のハンドラ")
        print(data)
        return False

    def isPublic(self):
        return False

