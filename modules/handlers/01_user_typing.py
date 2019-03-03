from modules.handlers import MsgHandler

class Handler(MsgHandler):
    def name(self):
        return "user_typing"

    def description(self):
        return "入力中メッセージを処理する"
    
    def isPublic(self):
        return False

    def eventType(self):
        return {'type': 'user_typing'}

    lastUser = ''
    lastCh = ''
    def process(self, sc, d):
        user = sc.getUsers()[d['user']]['name']
        ch = sc.getChannels()[d['channel']]['name']
        if self.lastUser == user and self.lastCh == ch:
            return False
        print(user, "is typing in", "#" + ch)
        self.lastUser = user
        self.lastCh = ch
        return False

