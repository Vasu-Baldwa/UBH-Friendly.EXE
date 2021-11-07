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


def main():
    x = threading.Thread(target=beaconHandler)
    x.start()
    port = 7025

if __name__ == "__main__":
    main()
