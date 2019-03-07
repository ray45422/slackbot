import json
from pathlib import Path
import os.path

basedir = Path(os.path.dirname(__file__) + "/../")

def loadJsonFromFile(fileName):
    fileName = basedir / fileName
    if not Path(fileName).is_file():
        return None
    f = open(fileName, "r")
    s = json.load(f)
    f.close()
    return s

def saveJson(obj, fileName):
    fileName = basedir / fileName
    f = open(fileName, "w")
    json.dump(obj, fp=f)
    f.close()

dataDir = basedir / "data"
errorDir = basedir / "errors"
if not dataDir.exists():
    dataDir.mkdir()
if not errorDir.exists():
    errorDir.mkdir()

