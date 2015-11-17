# coding=utf-8
__author__ = 'aztst40'

import sqlite3
import ConfigParser
import psycopg2
import urllib2
import json
from ast import literal_eval
from datetime import datetime

_APICALL=""
_DOWNLOAD=""
_LOGSTATISTIK=""
_AUTH_KEY=""
_RESOURCEID=""
_URL=""
_HOST=""
_DBNAME=""
_USER=""
_PASSWORD=""

def APICall():
    conn = sqlite3.connect(_LOGSTATISTIK)
    c = conn.cursor()

    with open(_APICALL) as f:
        purchases='['
        for line in f:
            iori=line.index('resource_id=')+12
            resource_id=line[iori:iori+36]
            date=line[41:52]
            ioa=line.index('/action/')+8
            ios=line.index('?',ioa)
            command=line[ioa:ios]
            purchases=purchases + '(\'' + resource_id + '\',\'' + date + '\',\'' + command + '\'),'
        purchases=purchases + "]"
    c.execute("delete from APICall;")
    conn.commit()
    tuble=l = literal_eval(purchases)
    c.executemany('INSERT INTO APICall VALUES (?,?,?)', tuble)
    conn.commit()
    conn.close()

def Download():
    conn = sqlite3.connect(_LOGSTATISTIK)
    c = conn.cursor()
    with open(_DOWNLOAD) as f:
        purchases='['
        for line in f:
            st=line.find('/download/')
            sl=line.find(' HTTP')
            if (st>-1) and (sl>-1):
                if line[st:sl].find('.php')==-1:
                    r=line.find('resource')
                    d=line.find('download')
                    resource=line[r+9:d-1]
                    date=line[41:52]		    
                    purchases=purchases + '(\'' + resource + '\',\'' + date + '\'),'
        purchases=purchases + "]"
    c.execute("delete from Download;")
    conn.commit()
    tuble=l = literal_eval(purchases)    
    c.executemany('INSERT INTO Download VALUES (?,?)', tuble)
    conn.commit()
    conn.close()

def ckandb2sqlite():
    conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (_HOST,_DBNAME,_USER,_PASSWORD)
    connpg = psycopg2.connect(conn_string)
    cursor = connpg.cursor()
    try:
        cursor.execute("""select id, name from resource where state='active';""")
    except:
        pass
    rows = cursor.fetchall()
    purchases='['
    for row in rows:
        purchases=purchases + '(\'' + str(row[0]) + '\',\'' + str(row[1]) + '\'),'      
    purchases=purchases + "]"
    connsl = sqlite3.connect(_LOGSTATISTIK)    
    c = connsl.cursor()
    c.execute("delete from Resources;")
    connsl.commit()
    connsl.text_factory=purchases
    tuble=l = literal_eval(purchases)
    c.executemany('INSERT INTO Resources VALUES (?,?)', tuble)
    connsl.commit()
    connsl.close()

def readConfigFile():
    Config = ConfigParser.ConfigParser()
    Config.read("/home/deploy/bin_script/LogStatistik/DKAarhuskommuneODAA.ini")
    global _APICALL
    global _DOWNLOAD
    global _LOGSTATISTIK
    global _AUTH_KEY
    global _RESOURCEID
    global _URL
    global _HOST
    global _DBNAME
    global _USER
    global _PASSWORD
    _APICALL=Config.get("LogStatistik","APICALL")
    _DOWNLOAD=Config.get("LogStatistik","DOWNLOAD")
    _LOGSTATISTIK=Config.get("LogStatistik","LOGSTATISTIK")
    _AUTH_KEY=Config.get("LogStatistik","AUTH_KEY")
    _RESOURCEID=Config.get("LogStatistik","RESOURCEID")
    _URL=Config.get("LogStatistik","URL")
    _HOST=Config.get("LogStatistik","HOST")
    _DBNAME=Config.get("LogStatistik","DBNAME")
    _USER=Config.get("LogStatistik","USER")
    _PASSWORD=Config.get("LogStatistik","PASSWORD")


def sqlite2CKAN():
    headers = {'content-type': 'application/json', 'Authorization': _AUTH_KEY}

    connsl = sqlite3.connect(_LOGSTATISTIK)
    c = connsl.cursor()

    sql="""select count(name) as c,name,logdate,Resources.resource_id,'API' as type from Resources inner join APICall on Resources.resource_id=APICall.resource_id group by name
    union all
    select count(name) as c,name,logdate,Resources.resource_id,'Download' as type from Resources inner join Download on Resources.resource_id=Download.resource_id group by name order by c desc;
    """
    i = datetime.now()
    cursor = c.execute(sql)
    all_rows = cursor.fetchall()
    datastore_structure = """{"resource_id": "%s",
                      "fields":[{"id": "date"},{"id":"count"}, {"id":"name"}, {"id": "logdate"}, {"id": "resource_id"}, {"id": "type"}],
                      "records":[""" % _RESOURCEID
    for row in all_rows:
        date=i.strftime('%Y/%m/%d %H:%M:%S')
        datastore_structure +="""{"date": "%s","count":"%s", "name": "%s", "logdate": "%s", "resource_id": "%s", "type": "%s"},""" % (date,row[0],row[1].replace("\"","\\\"").replace("\n",""),row[2],row[3],row[4])
    datastore_structure = datastore_structure[:-1]
    datastore_structure +="""],"force":"true"}"""
    datastore_structure=datastore_structure.encode('utf-8')
    d = json.loads(datastore_structure)   
    req = urllib2.Request(_URL + 'datastore_create', data=json.dumps(d), headers=headers)
    response = urllib2.urlopen(req)

def main():
    readConfigFile()
    Download()
    APICall()
    ckandb2sqlite()
    sqlite2CKAN()

if __name__ == "__main__":
    main()
