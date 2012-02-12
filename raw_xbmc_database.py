import os, xbmc
from utilities import Debug
#provides access to the raw xbmc video database


global _RawXbmcDb__conn
_RawXbmcDb__conn = None
class RawXbmcDb():

    # make a httpapi based XBMC db query (get data)
    @staticmethod
    def query(query):
        global _RawXbmcDb__conn
        if _RawXbmcDb__conn is None:
            _RawXbmcDb__conn = _findXbmcDb()

        Debug("[RawXbmcDb] query: "+query)
        cursor = _RawXbmcDb__conn.cursor()
        cursor.execute(query)

        matches = []
        for row in cursor:
            matches.append(row)
        
        Debug("[RawXbmcDb] matches: "+unicode(matches))

        _RawXbmcDb__conn.commit()
        cursor.close()
        return matches

    # execute a httpapi based XBMC db query (set data)
    @staticmethod
    def execute(query):
        global _RawXbmcDb__conn
        if _RawXbmcDb__conn is None:
            _RawXbmcDb__conn = _findXbmcDb()
        cursor = _RawXbmcDb__conn.cursor()
        Debug("[RawXbmcDb] query: "+query)
        cursor.execute(query)

def _findXbmcDb():
    type = None
    host = None
    port = 3306
    name = None
    user = None
    passwd = None
    if not os.path.exists(xbmc.translatePath("special://userdata/advancedsettings.xml")):
        type = 'sqlite3'
    else:
        from xml.etree.ElementTree import ElementTree
        advancedsettings = ElementTree()
        advancedsettings.parse(xbmc.translatePath("special://userdata/advancedsettings.xml"))
        settings = advancedsettings.getroot().find("videodatabase")
        if settings is not None:
            for setting in settings:
                if setting.tag == 'type':
                    type = setting.text
                elif setting.tag == 'host':
                    host = setting.text
                elif setting.tag == 'port':
                    port = setting.text
                elif setting.tag == 'name':
                    name = setting.text
                elif setting.tag == 'user':
                    user = setting.text
                elif setting.tag == 'pass':
                    passwd = setting.text
        else:
            type = 'sqlite3'
    
    if type == 'sqlite3':
        if host is None:
            path = xbmc.translatePath("special://userdata/database")
            files = os.listdir(path)
            latest = ""
            for file in files:
                if file[:8] == 'MyVideos':
                    if file > latest:
                        latest = file
            Debug(latest)
            host = os.path.join(path,latest)
        else:
            host += ".db"
        import sqlite3
        return sqlite3.connect(host)
    if type == 'mysql':
        import mysql.connector
        return mysql.connector.Connect(host = host, port = port, database = name, user = user, password = passwd)
        