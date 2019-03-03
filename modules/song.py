import unicodedata
import re
import MeCab

mecab = MeCab.Tagger("-d /usr/lib/mecab/dic/mecab-ipadic-neologd")

def canSplit(p1, p2):
    c1 = p1[0][-1]
    c2 = p2[0][0]
    name1 = unicodedata.name(c1)
    name2 = unicodedata.name(c2)
    if name1.startswith("HIRAGANA") and not name2.startswith("HIRAGANA"):
        return True
    if p2[2] == '自立':
        return True
    if p2[1] == '名詞':
        return True
    if p2[1] == '連体詞':
        return True
    if p2[1] == '感動詞':
        return True
    if p1[2] == '接続助詞':
        return True
    return False

def parse(text):
    result = mecab.parse(text).split("\n")
    while result.pop() != "EOS":
        pass
    lst = []
    for l in result:
        r = l.split("\t")
        r = [r[0]] + r[1].split(",")
        if r[1] == '記号':
            continue
        lst.append(r)
    return lst

def split(text):
    stcs = []
    lst = parse(text)
    if len(lst) == 0:
        return stcs
    for l in lst:
        print(str(l))
    stc = [lst[0]]
    for i in range(1, len(lst)):
        if canSplit(lst[i - 1], lst[i]):
            stcs.append(stc)
            stc = []
        stc.append(lst[i])
    stcs.append(stc)
    return stcs

def matchPattern(stcs, pattern=[5, 7, 5]):
    msgs = []
    if len(stcs) == 0:
        return (False, msgs)
    count = 0
    patIdx = 0
    long = 0
    patYomi = ""
    for p in stcs:
        if patIdx >= len(pattern):
            return (False, msgs)
        yomi = ""
        for s in p:
            if len(s) != 10:
                yomi += s[0]
            else:
                yomi += s[-1]
        length = len(yomi)
        small = length - len(re.sub("[ァィゥェォャュョ]", "", yomi))
        if yomi.endswith("ー"):
            long += 1
        count += length - small
        patYomi += yomi
        if (count -long) <= pattern[patIdx] <= count:
            msgs.append(patYomi)
            patYomi = ""
            patIdx += 1
            long = 0
            count = 0
        elif count > pattern[patIdx]:
            return (False, msgs)
    if patIdx == len(pattern):
        return (True, msgs)
    return (False, msgs)

def isHaiku(stcs):
    ret = matchPattern(stcs, [5, 7, 5])
    if ret[0]:
        print("短歌です")
    return ret

def isTanka(stcs):
    ret = matchPattern(stcs, [5, 7, 5, 7, 7])
    if ret[0]:
        print("短歌です")
    return ret

if __name__ == '__main__':
    from pprint import pprint
    try:
        while True:
            print(">", end="")
            p = input()
            if p =='':
                continue
            stcs = split(p)
            pprint(stcs)
            pprint(matchPattern(stcs))
            pprint(matchPattern(stcs, [5, 7, 5, 7, 7]))
    except KeyboardInterrupt:
        pass

