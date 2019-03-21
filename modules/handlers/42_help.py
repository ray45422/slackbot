import modules.handlers as handlers
import re

class Handler(handlers.MsgHandler):
    def name(self):
        return "help"

    def description(self):
        return "この機能です。「help コマンド名」とすると各コマンドの詳しい説明を確認できます。"

    def descriptionDetail(self):
        return """>help [コマンド名]
コマンド名: helpで出てくるコマンド名を使用してください。
"""
    
    def eventType(self):
        return {'type': 'message', 'subtype': None}

    def isPublic(self):
        return True

    pattern = re.compile("(help|man)(\s+(?P<cmd>.+))?")
    def process(self, sc, data):
        text = data['text']
        mat = self.pattern.match(text)
        if mat is None:
            return True
        cmd = mat.groupdict()['cmd']
        msgs = []
        all = False
        if cmd is not None:
            if cmd == "all":
                all = True
            else:
                handler = handlers.getHandler(cmd)
                if handler is None:
                    sc.rtm_send_message(data['channel'], "指定されたコマンドが見つかりません(" + cmd + ")")
                    return False
                sc.rtm_send_message(data['channel'], handler.descriptionDetail())
                return False
        keys = sorted(handlers.handlers)
        for key in keys:
            h = handlers.handlers[key]
            if not all and not h.isPublic():
                continue
            msg = str(h.priority()) + " " + h.name() + ": " + h.description()
            msgs.append(msg)
        sc.rtm_send_message(data['channel'], "\n".join(msgs))
        return False

