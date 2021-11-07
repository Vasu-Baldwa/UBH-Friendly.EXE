import sqlite3
import json
import base64

from sqlite3 import Error

UID = 0

def sql_connection():

    try:

        con = sqlite3.connect('mydatabase.db')

        return con

    except Error:

        print(Error)

def sql_table(con):

    cursorObj = con.cursor()

    #if beacon int = 1 -> it's a beacon call back
    cursorObj.execute("CREATE TABLE agents(beacon int, ip text, hostname text, username text, time text, commandResult text, MAC text PRIMARY KEY)")

    con.commit()

def main():
    con = sql_connection()
    sql_table(con)

    data = "eyJUeXBlIjp0cnVlLCJkZXZJcCI6IjEwLjg0LjkzLjMiLCJIb3N0bmFtZSI6InBhcnJvdCIsInVzZXJuYW1lIjoiVmFzdSIsInRpbWUiOiIyMDIxLTExLTA3IDAzOjI5OjQzIiwiUmVzdWx0Ijoie0ZST00gRlVOQ30iLCJNYWMiOiJkODpjNDo5Nzo5YTpjZTowMiAzMDpkMTo2YjpkODowZjpkZiJ9"

    decodedValue = str(base64.b64decode(data).decode('utf-8'))

    jsonStr = json.loads(decodedValue)



main()



#Vasu Laptop test str
"""
eyJUeXBlIjp0cnVlLCJkZXZJcCI6IjEwLjg0LjkzLjMiLCJIb3N0bmFtZSI6InBhcnJvdCIsInVzZXJuYW1lIjoiVmFzdSIsInRpbWUiOiIyMDIxLTExLTA3IDAzOjI5OjQzIiwiUmVzdWx0Ijoie0ZST00gRlVOQ30iLCJNYWMiOiJkODpjNDo5Nzo5YTpjZTowMiAzMDpkMTo2YjpkODowZjpkZiJ9
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

