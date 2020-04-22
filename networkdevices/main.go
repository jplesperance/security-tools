package main

import (
	"fmt"
	"github.com/google/gopacket"
	"log"
)

func main() {
	devices, err := pcap.FindAllDevs()
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Devices Found: ")
	for _, device := range devices {
		fmt.Println("\nName: ", device.Name)
		fmt.Println("Description: ", device.Description)
		fmt.Println("Devices Addresses: ")
		for _, address := range device.Addresses {
			fmt.Println("- IP Address: ", address.IP)
			fmt.Println("- Subnet Mast: ", address.Netmask)
		}
	}
}
