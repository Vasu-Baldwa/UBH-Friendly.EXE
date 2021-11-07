# I'm Malav and I can't get python to work
import socket
import select
import string
import sys
import os
import subprocess
import base64
import threading


def beaconHandler():
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 65321        # Port to listen on (non-privileged ports are > 1023)

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
                print(str(base64.b64decode(data).decode('utf-8')))
                conn.close()

# Helper function (formatting)


def display():
    # sys.stdout.write()
    sys.stdout.flush()


def main():
    if len(sys.argv) < 2:
        print("error")
    else:
        host = sys.argv[1]
#		name = str.encode(sys.argv[2])

    x = threading.Thread(target=beaconHandler)
    x.start()
    port = 7025
    # asks for user name
    # name=raw_input("\33[34m\33[1m CREATING NEW ID:\n Enter username: \33[0m")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # s.settimeout(2)
    # connecting host
    try:
        s.connect((host, port))
    except:
        print("Can't connect to the server")
        sys.exit()

# if connected
    # s.send(name)
    display()
    while 1:
        socket_list = [sys.stdin, s]

        # Get the list of sockets which are readable
        rList, wList, error_list = select.select(socket_list, [], [])

        for sock in rList:
            if sock == s:
                data = (sock.recv(4096)).decode('utf-8')
                if not data:
                    print('DISCONNECTED!!')
                    sys.exit()
                else:
                    #					resp = data.split("$")
                    #					if(resp[0].strip() == "exec"):
                    #						recv = resp[1]
                    print(str(base64.b64decode(data).decode('utf-8')))
                    # print(data)
                    # where client receives command
#						res = run_command(recv)

                    # send command
#						s.send(res)

        # user entered a message
            else:
                msg = sys.stdin.readline()
                s.send(str(msg).encode('utf-8'))
                # display()


"""
Runs command send from server with exec
"""


def run_command(cmd):
    result = subprocess.check_output(cmd, shell=True)
    return result


if __name__ == "__main__":
    main()
