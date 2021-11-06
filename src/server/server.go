package main

import (
    "bufio"
    "fmt"
    "log"
    "net"
    "os"
)
const (
	connHost = "localhost"
	connPort = "7025"
	connType = "tcp"
)

func WhenConnectedClient(conn net.Conn) {
    buffer, err := bufio.NewReader(conn).ReadBytes('\n')

    if err != nil {
        fmt.Println("Client left.")
        conn.Close()
        return
    }

    log.Println("Client message:", string(buffer[:len(buffer)-1]))

    conn.Write(buffer)

    WhenConnectedClient(conn)
}

func main() {
	fmt.Println("Starting " + connType + " server on " + connHost + ":" + connPort)
	server, err := net.Listen(connType, connHost+":"+connPort)

	if err != nil {
		fmt.Println("Error listening:", err.Error())
		os.Exit(1)
	}

	defer server.Close()

	for {
		client, err := server.Accept()
		if err != nil {
			fmt.Println("Error connecting:", err.Error())
			return
		}
		fmt.Println("Client connected.")

		fmt.Println("Client " + client.RemoteAddr().String() + " connected.")

		go WhenConnectedClient(client)
	}
}
