import psycopg2
import urllib2
import json
from datetime import datetime

def getResourceList():
    auth_key = 'xxxx'
    headers = {'content-type': 'application/json', 'Authorization': auth_key}

    url = "http://www.odaa.dk/api/3/action/"
    datastore_structure="{\"resource_id\":\"c81046d7-5071-4e42-aa5d-ed949bcfc250\",\"force\":\"true\"}"

    headers = {'content-type': 'application/json', 'Authorization': auth_key}
    d = json.loads(datastore_structure)
    req = urllib2.Request(url + 'datastore_delete',data=json.dumps(d),  headers=headers)
    try:
        response = urllib2.urlopen(req)
        response.close()
    except urllib2.URLError as e:
        print e
        pass   

    i = datetime.now()
    conn_string = "host='localhost' dbname='ckan_default' user='ckan_default' password='xxxx'"
    connpg = psycopg2.connect(conn_string)
    cursor = connpg.cursor()
    try:
         cursor.execute("""select r.name,r.created,r.id,r.package_id from resource as r inner join package as p on p.id=r.package_id where p.private=False and r.state<>'deleted' and p.state='active';""")
    except Exception, e:
        pass
    all_rows = cursor.fetchall()
    datastore_structure = """{"resource_id": "c81046d7-5071-4e42-aa5d-ed949bcfc250",
                      "fields":[{"id": "date"},{"id":"name"},{"id":"created"},{"id":"resource_id"}, {"id": "package_id"}],
                      "records":["""
    for row in all_rows:
        date=i.strftime('%Y/%m/%d %H:%M:%S')
        datastore_structure +="""{"date": "%s","name":"%s","created":"%s", "resource_id": "%s", "package_id": "%s"},""" % (date,row[0].replace("\"","\\\""),row[1],row[2],row[3])
    datastore_structure = datastore_structure[:-1]
    datastore_structure +="""],"force":"true"}"""
    
    d = json.loads(datastore_structure)        
    req = urllib2.Request(url + 'datastore_create', data=json.dumps(d), headers=headers)    
    try:
        response = urllib2.urlopen(req)
        response.close()
    except urllib2.URLError as e:
        print e
        pass
#    finally:
#        response.close()

def main():
    getResourceList()

if __name__ == "__main__":
    main()