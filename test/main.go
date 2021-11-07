package main

import (
	"encoding/json"
	"fmt"
	"net"
	"os"
	"os/user"
	"strings"
	"time"
	"encoding/base64"
)

type Packet struct {
	Type     bool   `json:"Type"`
	DevIP    string `json:"devIp"`
	Hostname string `json:"Hostname"`
	Username string `json:"username"`
	Time     string `json:"time"`
	Result   string `json:"Result"`
	Mac      string `json:"Mac"`
}

// func getPublicIP() string {
//     req, err := http.Get("http://ip-api.com/json/")
//     if err != nil {
//         return err.Error()
//     }
//     defer req.Body.Close()

//     body, err := ioutil.ReadAll(req.Body)
//     if err != nil {
//         return err.Error()
//     }

//     var ip IP
//     json.Unmarshal(body, &ip)

//     return ip.Query
// }

// func getIP() string {
// 	var ip net.IP

// 	ifaces, err := net.Interfaces()
// 	if err != nil {
// 		fmt.Println(err)
// 	}
// 	// handle err
// 	for _, i := range ifaces {
// 		addrs, err := i.Addrs()
// 		// handle err
// 		if err != nil {
// 			fmt.Println(err)
// 		}
// 		for _, addr := range addrs {
// 			switch v := addr.(type) {
// 			case *net.IPNet:
// 				ip = v.IP
// 			case *net.IPAddr:
// 				ip = v.IP
// 			}
// 			// process IP address
// 		}
// 	}

// 	return string(ip)
// }

func getLocalIP() net.IP {
    conn, err := net.Dial("udp", "8.8.8.8:80")
    if err != nil {
        fmt.Println(err)
    }
    defer conn.Close()

    localAddr := conn.LocalAddr().(*net.UDPAddr)

    return localAddr.IP
}

func getMacAddr() []string {
	ifas, err := net.Interfaces()
	if err != nil {
		fmt.Println(err)
	}
	var as []string
	for _, ifa := range ifas {
		a := ifa.HardwareAddr.String()
		if a != "" {
			as = append(as, a)
		}
	}
	return as
}

func getHostname() string {
	os, err := os.Hostname()
	if err != nil {
		fmt.Println(err)
	}
	return os
}

func getUsername() string {
	name, err := user.Current()
	if err != nil {
		fmt.Println(err)
	}
	return name.Name
}

func arrToString(strArray []string) string {
	return strings.Join(strArray, " ")
}

func main() {

	sendData := Packet{
		Type:     true,
		DevIP:    getLocalIP().String(),
		Hostname: getHostname(),
		Username: getUsername(),
		Time:     time.Now().UTC().Format("2006-01-02 15:04:05"),
		Result:   "{FROM FUNC}",
		Mac:      arrToString(getMacAddr()),
	}

	dat, err := json.Marshal(sendData)
	if err != nil {
		fmt.Println(err)
	}

	encoded := base64.StdEncoding.EncodeToString([]byte(dat))

	fmt.Println(encoded)

}
