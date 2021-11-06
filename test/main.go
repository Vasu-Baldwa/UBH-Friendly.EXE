package main

import(
	"fmt"
    "encoding/json"
	"os"
	"time"
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

func getPublicIP() string {
    req, err := http.Get("http://ip-api.com/json/")
    if err != nil {
        return err.Error()
    }
    defer req.Body.Close()

    body, err := ioutil.ReadAll(req.Body)
    if err != nil {
        return err.Error()
    }

    var ip IP
    json.Unmarshal(body, &ip)

    return ip.Query
}

func getIP() string{
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

	return string(ip)
}

func getMacAddr() ([]string, error) {
    ifas, err := net.Interfaces()
    if err != nil {
        return nil, err
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

func main(){

	sendData := Packet{
		Type: true,
		DevIP: getIP(),
		Hostname: os.Hostname(), //TURN TO FUNC (?)
		Username: os.user.Current(), //TURN TO FUNC(?)
		Time: time.Now().UTC().Format("2006-01-02 15:04:05"),
		Result: {FROM FUNC},
		Mac: getMacAddr(),
	}

	dat, err := json.Marshal(c)
if err != nil {
    return err
}



}