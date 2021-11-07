import sqlite3
import json
import base64

from sqlite3 import Error

def sql_connection():

    try:

        con = sqlite3.connect('mydatabase.db')

        return con

    except Error:

        print(Error)

def sql_init(con):

    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE beacons(uid int PRIMARY KEY, MAC text, Hostname text, Username text, ip text, lastseen text)")
    cursorObj.execute("CREATE TABLE commands(uid int PRIMARY KEY, command text, result text)")
    con.commit()


def sql_insertBeacon(con, entity):

    cursorObj = con.cursor()
    cursorObj.execute('INSERT INTO beacons(uid, MAC, Hostname, Username, ip, lastseen) VALUES(?, ?, ?, ?, ?, ?)', entity)
    con.commit()

def sql_updateBeacon(con, entity, mac):
    cursorObj = con.cursor()
    cursorObj.execute('UPDATE beacons SET (Hostname, ip, lastseen) VALUES (?,?,?) where MAC = ' + str(mac), entity)
    con.commit()

def noBeacon(con, mac):
    #return true if no beacon exists
    cursorObj = con.cursor()
    cursorObj.execute("SELECT uid FROM beacons WHERE MAC = " + str(mac))
    con.commit()
    if(cursorObj == None):
        return True
    return False
    

def main():

    UID = 0

    con = sql_connection()
    sql_init(con)

    data = "eyJUeXBlIjpmYWxzZSwiZGV2SXAiOiIxMC44NC45My4zIiwiSG9zdG5hbWUiOiJwYXJyb3QiLCJ1c2VybmFtZSI6IlZhc3UiLCJ0aW1lIjoiMjAyMS0xMS0wNyAwNDo0Nzo0NiIsIlJlc3VsdCI6Ii9ob21lL3N5c2FkbWluL1VCSC1GcmllbmRseS5FWEVcbiIsIk1hYyI6ImQ4OmM0Ojk3OjlhOmNlOjAyIDMwOmQxOjZiOmQ4OjBmOmRmIn0="

    decodedValue = str(base64.b64decode(data).decode('utf-8'))

    jsonStr = json.loads(decodedValue)

    if(jsonStr["Type"] == True):
        if(noBeacon(con, jsonStr["Mac"])):
            entities = (UID, jsonStr["Mac"], jsonStr["Hostname"], jsonStr["username"], jsonStr["devIp"], jsonStr["time"])
            sql_insertBeacon(con, entities)
            UID = UID+1
        else:
            entities = (jsonStr["Hostname"],jsonStr["devIp"], jsonStr["time"])
            sql_updateBeacon(con, entities, jsonStr["Mac"])

    else:
        print("Error")


    




main()



#Vasu Laptop test str
"""
eyJUeXBlIjpmYWxzZSwiZGV2SXAiOiIxMC44NC45My4zIiwiSG9zdG5hbWUiOiJwYXJyb3QiLCJ1c2VybmFtZSI6IlZhc3UiLCJ0aW1lIjoiMjAyMS0xMS0wNyAwNDo0Nzo0NiIsIlJlc3VsdCI6Ii9ob21lL3N5c2FkbWluL1VCSC1GcmllbmRseS5FWEVcbiIsIk1hYyI6ImQ4OmM0Ojk3OjlhOmNlOjAyIDMwOmQxOjZiOmQ4OjBmOmRmIn0=
"""




"""
What we need:


Beacon table
    UID
    MAC ID
    Hostname
    Username
    IP
    Last Seen

Commands History
    Result
    Time Run
    UID

{'Type': False, 'devIp': '10.84.93.3', 'Hostname': 'parrot', 'username': 'Vasu', 'time': '2021-11-07 04:47:46', 'Result': '/home/sysadmin/UBH-Friendly.EXE\n', 'Mac': 'd8:c4:97:9a:ce:02 30:d1:6b:d8:0f:df'}


"""

