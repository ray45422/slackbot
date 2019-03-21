import unicodedata
import re
import MeCab
from modules.handlers import MsgHandler
import modules.song as song

class Handler(MsgHandler):
    def name(self):
        return "song"

    def description(self):
        return "メッセージが俳句か短歌であると思われる場合にリアクションします"

    def isPublic(self):
        return True
    
    def eventType(self):
        return {'type': 'message', 'subtype': None}

    def process(self, sc, data):
        text = data['text']
        ch = data['channel']
        chStr = "<#" + ch + ">"
        ts = data['ts']
        stcs = song.split(text)
        ret = song.isHaiku(stcs)
        if ret[0]:
            sc.addReactions(ch, ts, ["haiku"])
            sc.rtm_send_message(sc.notifyCh, chStr + "\n俳句を検出しました\n" + "\n".join(ret[1]))
        ret = song.isTanka(stcs)
        if ret[0]:
            sc.addReactions(ch, ts, ["tanka"])
            sc.rtm_send_message(sc.notifyCh, chStr + "\n短歌を検出しました\n" + "\n".join(ret[1]))
        return True

