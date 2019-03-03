import re
import html
from modules.handlers import MsgHandler

class Handler(MsgHandler):
    def name(self):
        return "message"

    def description(self):
        return "メッセージの前処理を行います"
    
    def eventType(self):
        return {'type': 'message', 'subtype': None}

    def isPublic(self):
        return False

    def process(self, sc, data):
        if "subtype" in data:
            print("subype:", data['subtype'])
        data['text'] = html.unescape(data['text'])
        return True

