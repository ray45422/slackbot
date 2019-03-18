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
        user = sc.getUserByID(d['user'])
        ch = sc.getChannelByID(d['channel'])
        if user or ch:
            return False
        user = user['name']
        ch = ch['name']
        if self.lastUser == user and self.lastCh == ch:
            return False
        print(user, "is typing in", "#" + ch)
        self.lastUser = user
        self.lastCh = ch
        return False

