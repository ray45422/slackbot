import json
import os.path
import random
import re
import urllib.parse

from . import datautil

def get(key):
    return list[key]

def set(key, value):
    list[key] = value
    save()

def remove(key):
    ret = remove_impl(key)
    if ret == None:
        return None
    save()
    return ret

def remove_impl(key):
    if isExists(key):
        return list.pop(key)
    try:
        index = int(key) - 1
    except ValueError:
        print("数値変換エラー")
        return None
    print("index:",index)
    print("len:", len(list))
    if index >= 0 and index < len(list):
        key = [*list][index]
        return list.pop(key)
    print("インデックスが超えてます")
    return None

def isExists(key):
    return key in list.keys()

def getResponse(text):
    for v in list.items():
        regex = re.compile(v[0])
        if not regex.search(text):
            continue
        l = v[1]
        resp = l[random.randint(0, len(l) - 1)]
        resp = respSub(text, resp, regex)
        return resp
    return None

def respSub(text, resp, regex):
    mat = regex.match(text)
    print(mat)
    print(regex)
    if mat is None:
        return resp
    pats = re.findall(r"(\\g<(?:(\w+)(?:\s*,\s*(\w+))?)>)", resp)
    print(pats)
    for pat in pats:
        print(pat)
        repl = mat.expand(r"\\g<" + pat[1] + ">")
        repl = getConvFunc(pat[2])(repl)
        resp = resp.replace(pat[0], repl)
    return mat.expand(resp)

def getConvFunc(name):
    if name == 'perenc':
        return lambda s: urllib.parse.quote(s)
    if name == 'test':
        return lambda s: s + 'test'
    return lambda s: s



def load():
    global list
    list = datautil.loadJsonFromFile(file)
    if list == None:
        list = {}
        save()

def save():
    datautil.saveJson(list, file)

file = "data/response.json"
load()

