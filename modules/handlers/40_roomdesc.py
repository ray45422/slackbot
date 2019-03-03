import re
from modules.handlers import MsgHandler

class Handler(MsgHandler):
    def name(self):
        return "roomdesc"

    def description(self):
        return "「部屋紹介」というと部屋の一覧と紹介を表示します"
    
    def eventType(self):
        return {'type': 'message', 'subtype': None}

    def isPublic(self):
        return True

    def process(self, sc, data):
        if data['text'] != "部屋紹介":
            return True
        msgs = []
        for t in sorted(sc.getChannels().items(), key=lambda t: t[1]['name']):
            ch = t[1]
            if ch['is_archived']:
                continue
            purpose = ch['purpose']['value']
            emojiRe = ':[^:]+:'
            emoji = re.sub('^(' + emojiRe + ')?.*', '\\1', purpose)
            if emoji == '':
                emoji = ":space:"
            purpose = re.sub('^(' + emoji + ')\\s*', '', purpose)
            msg = emoji + " <#" + ch['id'] + "|" + ch['name'] + "> " + purpose
            msgs.append(msg)
        sc.rtm_send_message(data['channel'], "\n".join(msgs))
        return False

