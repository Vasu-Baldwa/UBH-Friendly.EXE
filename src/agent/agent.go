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
	connHost = "localhost"
	connPort = "7025"
	connType = "tcp"
)

func handleConnection(conn net.Conn) {
	buffer, err := bufio.NewReader(conn).ReadString('\n')
	print(buffer)
	if err != nil {
		fmt.Println("Client left.")
		conn.Close()
		return
	}
	//newCmd := strings.TrimSuffix(buffer, "\n")
	//todo: seperate command and args
	//print(newCmd)
	buffer = strings.Replace(buffer, "\n", "", -1)
	command, err := exec.Command(buffer).Output()

	if err != nil {
		fmt.Println(err)
		conn.Close()
		return
	}
	print(string(command))
}

func main() {
	//fmt.Println("Starting " + connType + " server on " + connHost + ":" + connPort)
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
