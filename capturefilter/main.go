package main

import (
	"fmt"
	"github.com/google/gopacket"
	"github.com/google/gopacket/pcap"
	"log"
	"os"
	"time"
	"flag"
	"strconv"
)

var (
	device            = flag.String("device", "eth0", "the network device to use")
	snapshotLen int32 = 1024
	promiscuous       = flag.Bool("promiscuous", false, "use promiscuous mode")
	err         error
	timeout     = 30 * time.Second
	handle      *pcap.Handle
	mode			= flag.String("mode", "monitor", "monitor: display output to console; \nlogged: logs output to file;\n hybrid: monitor and logged modes")
	protocol		= flag.String("protocol", "tcp", "tcp or udp")
	port			= flag.Int("port", 80, "the port to capture traffic on")
)

func main() {
	flag.Parse()
	handle, err := pcap.OpenLive(*device, snapshotLen, *promiscuous, timeout)
	if err != nil {
		log.Fatal(err)
	}
	defer handle.Close()
	logFile, err := os.OpenFile("capture.txt", os.O_RDWR|os.O_CREATE|os.O_APPEND, 0666)
	if err != nil {
		panic(err)
	}
	defer logFile.Close()
	logger := log.New(logFile, "", log.LstdFlags)
	var filter string = *protocol + " and port " + strconv.Itoa(*port)
	err = handle.SetBPFFilter(filter)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("Only capturing "+*protocol+" port "+strconv.Itoa(*port)+" packets")

	packetSource := gopacket.NewPacketSource(handle, handle.LinkType())


	for packet := range packetSource.Packets() {
		if *mode == "monitor" || *mode == "hybrid" {
			fmt.Println(packet)
		}
		if *mode == "logged" || *mode == "hybrid" {
			logger.Println(packet)
		}
	}
}
