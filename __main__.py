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

notifych = None
myuserid = None
for ch in slack.client.getChannels().values():
    if ch['name'] == 'botdevelop':
        notifych = ch['id']
        break
for user in slack.client.getUsers().values():
    if user['name'] == 'ray45422':
        myuserid = user['id']
        break
if notifych == None or myuserid == None:
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
            name = "error" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".txt"
            f = open(datautil.errorDir / name, 'w')
            f.write(traceback.format_exc())
            f.close()
            msg = "<@" + slack.getClient().notifyUserID + ">"
            msg += " エラーが発生しました。\n"
            msg += str(e)
            msg += "\n"
            msg += name
            sc.rtm_send_message(slack.getClient().notifyCh, msg)

except KeyboardInterrupt:
    print("finish")


print(datetime.datetime.today())

