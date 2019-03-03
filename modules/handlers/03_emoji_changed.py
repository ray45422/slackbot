from modules.handlers import MsgHandler

class Handler(MsgHandler):
    def name(self):
        return "emoji_changed"

    def description(self):
        return "絵文字変更イベントを処理する"
    
    def isPublic(self):
        return False

    def eventType(self):
        return {'type': 'emoji_changed'}
    
    def process(self, sc, d):
        st = d['subtype']
        if st == 'add':
            print("絵文字が追加されました")
        if st == 'remove':
            print("絵文字が削除されました")
        return False

