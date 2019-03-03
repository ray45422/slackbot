from modules.handlers import MsgHandler

class Handler(MsgHandler):
    def name(self):
        return "desktop_notify"

    def description(self):
        return "デスクトップ通知イベントを処理する"
    
    def isPublic(self):
        return False

    def eventType(self):
        return {'type': 'desktop_notification'}
    
    def process(self, sc, d):
        return False

