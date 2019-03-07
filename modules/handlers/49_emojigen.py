import re
from modules.handlers import MsgHandler
import sys
path = "/srv/slack/emojigen"
if path not in sys.path:
    sys.path.append("/srv/slack/emojigen")
import emojigen


class Handler(MsgHandler):
    regex = re.compile("emojigen\s+(?P<name>\w+)\s+(?P<text>.+)\s+(?P<color>#[0-9a-fA-F]{6})$")
    def description(self):
        return "絵文字を生成します"
    
    def eventType(self):
        return {'type': 'message', 'subtype': None}

    def isPublic(self):
        return True

    def process(self, sc, data):
        text = data['text']
        ch = data['channel']
        regex = self.regex
        if not text.startswith("emojigen"):
            return True
        mat = regex.match(text)
        if mat is None:
            sc.rtm_send_message(ch, ">emojigen name text color")
            return False
        dict = mat.groupdict()
        emojigen.createMojiEmoji(dict['name'], dict['text'], dict['color'])
        sc.rtm_send_message(ch, "<https://slack.ray45422.net/emoji/" + dict['name'] + ".png>")
        return False
