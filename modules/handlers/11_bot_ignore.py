from modules.handlers import MsgHandler

class Handler(MsgHandler):
    def name(self):
        return "bot_ignore"

    def description(self):
        return "botのメッセージを無視します"
    
    def eventType(self):
        return {'type': 'message', 'subtype': None}

    def isPublic(self):
        return False

    def process(self, sc, data):
        print(data)
        id = data['user']
        user = sc.getUserByID(id)
        if user is None or user['is_bot']:
            return False
        return True

