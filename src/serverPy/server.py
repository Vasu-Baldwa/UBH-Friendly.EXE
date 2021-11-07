# I'm Malav and I can't get python to work
import socket
import select
import string
import sys
import os
import subprocess
import base64
import threading
import json
import sqlite3

from sqlite3 import Error


def sql_connection():
    try:
        con = sqlite3.connect('mydatabase.db')
        return con
    except Error:
        print(Error)


def sql_init(con):
    cursorObj = con.cursor()
    cursorObj.execute(
        "CREATE TABLE beacons(uid int PRIMARY KEY, MAC text, Hostname text, Username text, ip text, lastseen text)")
    cursorObj.execute(
        "CREATE TABLE commands(uid int PRIMARY KEY, command text, result text)")
    con.commit()


def sql_insertBeacon(con, entity):
    cursorObj = con.cursor()
    cursorObj.execute(
        'INSERT INTO beacons(uid, MAC, Hostname, Username, ip, lastseen) VALUES(?, ?, ?, ?, ?, ?)', entity)
    con.commit()


def sql_updateBeacon(con, entity, mac):
    cursorObj = con.cursor()
    cursorObj.execute(
        'UPDATE beacons SET (Hostname, ip, lastseen) VALUES (?,?,?) where MAC = ' + str(mac), entity)
    con.commit()


def noBeacon(con, mac):
    # return true if no beacon exists
    cursorObj = con.cursor()
    cursorObj.execute("SELECT uid FROM beacons WHERE MAC = " + str(mac))
    con.commit()
    if(cursorObj == None):
        return True
    return False


def jsonVal(decodedValue):
    return json.loads(decodedValue)


def beaconHandler():
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 65321        # Port to listen on (non-privileged ports are > 1023)
    UID = 0
    con = sql_connection()
    sql_init(con)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        while True:
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                data = conn.recv(1024)
                if not data:
                    conn.close()
                # Beacon SQL Stuff
                jsonStr = jsonVal(str(base64.b64decode(data).decode('utf-8')))
                if(jsonStr["Type"] == True):
                    if(noBeacon(con, jsonStr["Mac"])):
                        entities = (UID, jsonStr["Mac"], jsonStr["Hostname"],
                                    jsonStr["username"], jsonStr["devIp"], jsonStr["time"])
                        sql_insertBeacon(con, entities)
                        UID = UID+1
                    else:
                        entities = (jsonStr["Hostname"],
                                    jsonStr["devIp"], jsonStr["time"])
                        sql_updateBeacon(con, entities, jsonStr["Mac"])
                else:
                    print("SQL ERROR")
                conn.close()

#########################################################################


def main():
    x = threading.Thread(target=beaconHandler)
    x.start()
    port = 7025


if __name__ == "__main__":
    main()
