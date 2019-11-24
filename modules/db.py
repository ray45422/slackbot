import sqlite3
import modules.datautil as datautil

dbFile = datautil.dataDir / "datafile.db"

class ConnectionPool:
    file = ''
    poolList = []
    usingList = []
    def __init__(self, file):
        self.file = file

    def getFile(self):
        return self.file

    def getConnection(self):
        if len(self.poolList) != 0:
            con = self.poolList.pop()
            self.usingList.append(con)
            return con
        con = sqlite3.connect(self.file)
        self.usingList.append(con)
        return con

    def releaseConnection(self, con):
        if con not in self.usingList:
            return False
        self.usingList.remove(con)
        self.poolList.append(con)
        return True

pools = {}

def getConnection(file = dbFile):
    if file not in pools:
        pools[file] = ConnectionPool(file)
    return pools[file].getConnection()

def execute(query, param=[]):
    return executeImpl(dbFile, query, param)

def executeImpl(file, query, param):
    con =  getConnection(file)
    result = con.execute(query, param)
    con.commit();
    pools[file].releaseConnection(con)
    return result

def releaseConnection(con):
    for pool in pools.values():
        if pool.releaseConnection(con):
            return

