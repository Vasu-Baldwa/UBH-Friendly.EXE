package main

import (
	"fmt"
	"net"
)

func main() {
	
	var ip net.IP

	ifaces, err := net.Interfaces()
	if err != nil{
		fmt.Println(err)
	}
	// handle err
	for _, i := range ifaces {
		addrs, err:= i.Addrs()
		// handle err
		if err != nil{
			fmt.Println(err)
		}
		for _, addr := range addrs {
			switch v := addr.(type) {
			case *net.IPNet:
					ip = v.IP
			case *net.IPAddr:
					ip = v.IP
			}
			// process IP address
		}
	}
	fmt.Println(ip);
}
