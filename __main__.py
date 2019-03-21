import datetime
import sys
import time
import traceback

import modules.slack as slack
import modules.datautil as datautil
import modules.handlers as handlers

sc = slack.client.sc
datautil.saveJson(slack.client.getChannels(), "data/channels.json")
datautil.saveJson(slack.client.getUsers(), "data/users.json")
datautil.saveJson(slack.client.getEmoji(), "data/emoji.json")

if slack.getClient().notifyCh == None or slack.getClient().notifyUserID == None:
    print("チャンネルもしくはユーザーID が取得できませんでした")
    exit()

if not sc.rtm_connect(auto_reconnect=True):
    print("connection failed")
    exit()
try:
    while sc.server.connected is True:
        sys.stdout.flush()
        data = sc.rtm_read()
        try:
            if len(data) == 0:
                time.sleep(0.1)
                continue
            for d in data:
                handlers.onEvent(slack.client, d)
        except Exception as e:
            if isinstance(e, handlers.HandlerException):
                tbstr = e.traceback
                author = slack.getClient().getUserByName(e.handler.author())
                emsg = str(e.exception)
            else:
                tbstr = traceback.format_exc()
                author = None
                emsg = str(e)

            name = "error" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".txt"
            f = open(datautil.errorDir / name, 'w')
            f.write(tbstr)
            f.close()
            msg = "<@" + slack.getClient().notifyUserID + ">"
            if author is not None and author['id'] != slack.getClient().notifyUserID:
                msg += "<@" + author['id'] + ">"
            msg += " エラーが発生しました。\n"
            msg += emsg
            msg += "\n"
            msg += name
            sc.rtm_send_message(slack.getClient().notifyCh, msg)

except KeyboardInterrupt:
    print("finish")


print(datetime.datetime.today())

