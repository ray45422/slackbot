import unicodedata
import re
import MeCab
from modules.handlers import MsgHandler
import modules.song as song

class Handler(MsgHandler):
    def name(self):
        return "song"

    def description(self):
        return "メッセージで俳句か短歌を見つけたときにリアクションします"

    def isPublic(self):
        return True
    
    def eventType(self):
        return {'type': 'message', 'subtype': None}

    def process(self, sc, data):
        text = data['text']
        ch = data['channel']
        ts = data['ts']
        stcs = song.split(text)
        ret = song.isHaiku(stcs)
        if ret[0]:
            sc.addReactions(ch, ts, ["haiku"])
            sc.rtm_send_message(sc.notifyCh, "俳句を検出しました\n" + "\n".join(ret[1]))
        ret = song.isTanka(stcs)
        if ret[0]:
            sc.addReactions(ch, ts, ["tanka"])
            sc.rtm_send_message(sc.notifyCh, "短歌を検出しました\n" + "\n".join(ret[1]))
        return True

