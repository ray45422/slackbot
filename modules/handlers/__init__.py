from pathlib import Path
from abc import ABCMeta, abstractmethod
import re
import importlib

class MsgHandler(metaclass=ABCMeta):
    _name = None
    _pri  = None
    def name(self):
        if self._name is not None:
            self._name
        mod = self.__class__.__module__.split(".").pop(-1)
        m = re.match("\d+_(?P<name>.+)", mod)
        if m is None:
            raise Exception("ファイル名が正しく指定されていません:" + mod)
        self._name = m.groupdict()['name']
        return self._name
    @abstractmethod
    def eventType(self):
        pass
    @abstractmethod
    def description(self):
        pass
    @abstractmethod
    def process(self, sc, data):
        pass
    @abstractmethod
    def isPublic(self):
        pass
    def priority(self):
        if self._pri is not None:
            return self._pri
        mod = self.__class__.__module__.split(".").pop(-1)
        m = re.match("(?P<pri>[0-9]+)_", mod)
        if m is None:
            raise Exception("優先度が指定されていません:" + self.name())
        self._pri = int(m.groupdict()['pri'])
        return self._pri


def _moduleLoad():
    reg = re.compile("\d+_.+")
    for f in Path(__file__).parent.glob("*.py"):
        name = f.stem
        if not reg.match(name):
            continue
        modules[name] = importlib.import_module('modules.handlers.' + name)

def addHandler(handler):
    if not isinstance(handler, MsgHandler):
        print("this object is not MsgHandler")
    handlers[handler.priority()] = handler

def getHandler(name):
    for h in handlers.values():
        if h.name == name:
            return h
    return None

def removeHandler(name):
    h = getHandler(name)
    if h == None:
        return None
    return handlers.remove(h)

def _load():
    for m in modules.values():
        h = m.Handler()
        addHandler(h)

def _clear():
    while(True):
        h = handlers.pop(0, None)
        if h is None:
            break
        del h

def _reload():
    _clear()
    _moduleLoad()
    for m in modules.items():
        modules[m[0]] = importlib.reload(m[1])
    _load()

def onEvent(sc, data):
    keys = sorted(handlers.keys())
    for key in keys:
        h = handlers[key]
        if not eventMatch(data, h):
            continue
        if not h.process(sc, data):
            return

def eventMatch(d, h):
    filter = h.eventType()
    for key in filter.keys():
        v = filter[key]
        if v == None:
            if key in d.keys():
                return False
            continue
        if key not in d.keys():
            return False
        if not re.match(v, d[key]):
            return False
    return True

__all__ = []
modules = {}
handlers = {}

_moduleLoad()
_load()

