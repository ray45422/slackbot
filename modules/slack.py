import re
import time
import os
import concurrent.futures
from slackclient import SlackClient

token1 = os.environ['SLACK_TOKEN']
token2 = os.environ['SLACK_OAUTH_TOKEN']

def getClient():
    return client

def getSC():
    return SlackClient(token1)

def addReactions(ch, names, ts):
    sc = getSC()
    for name in names:
        sc.api_call(
           "reactions.add",
            channel=ch,
            timestamp=ts,
            name=name
            )

class Slack():
    sc = SlackClient(token1)
    sco = SlackClient(token2)
    excutor = concurrent.futures.ThreadPoolExecutor()
    updateCoolTime = 60
    lastUpdate = {}
    channels = []
    users = []
    emoji = []
    myID = None
    myName = 'zumirobo'
    notifyCh = None
    notifyChName = 'botdevelop'
    notifyUserID = None
    notifyUserName = 'ray45422'
    def __del__(self):
        self.excutor.shutdown()
    def apiCall(self, *args, **kwargs):
        return self.excutor.submit(addReaction, args, kwargs)
    def rtm_send_message(self, ch, msg):
        return self.sc.rtm_send_message(ch, msg)
    def canUpdate(self, name):
        if name not in self.lastUpdate.keys():
            return True
        t = self.lastUpdate[name]
        if time.time() - t < self.updateCoolTime:
            return False
        return True
            
    def addReactions(self, ch, ts, names):
        future = self.excutor.submit(
            addReactions,
            ch=ch,
            ts=ts,
            names=names
            )
        return future
        #res = self.sc.api_call(
        #   "reactions.add",
        #    channel=ch,
        #    name=name,
        #    timestamp=ts
        #    )
        #return res
    def getChannels(self):
        if not self.canUpdate('ch'):
            return self.channels
        res = self.sc.api_call(
                "channels.list",
        )
        if not res['ok']:
            return []
        chs = {}
        for ch in res['channels']:
            chs[ch['id']] = ch
            if ch['name'] == self.notifyChName:
                self.notifyCh = ch['id']
        self.lastUpdate['ch'] = time.time()
        self.channels = chs
        return chs
    def getChannelByName(self, name):
        for ch in self.getChannels().values():
            if ch['name'] == name:
                return ch
        return None

    def getUsers(self):
        if not self.canUpdate('usr'):
            return self.users
        res = self.sc.api_call(
                "users.list",
        )
        if not res['ok']:
            return []
        users = {}
        for user in res['members']:
            users[user['id']] = user
            if user['name'] == self.myName:
                self.myID = user['id']
            if user['name'] == self.notifyUserName:
                self.notifyUserID = user['id']
        self.lastUpdate['usr'] = time.time()
        self.users = users
        return users
    def getUserByID(self, id):
        if id not in self.getUsers():
            return None
        return self.getUsers()[id]
    def getUserByName(self, name):
        for usr in self.getUsers().values():
            if usr['name'] == name:
                return usr
        return None

    def getEmoji(self):
        if not self.canUpdate('emoji'):
            return self.emoji
        res = self.sco.api_call(
                "emoji.list",
        )
        if not res['ok']:
            return []
        self.lastUpdate['emoji'] = time.time()
        self.emoji = res['emoji']
        return res['emoji']

    def isMention(self, data):
        if 'text' not in data:
            return False
        text = data['text']
        id = self.getUserByName(self.myName)
        if id is None:
            return False
        id = id['id']
        return re.search("<@" + id + ">", text) is not None

client = Slack()

