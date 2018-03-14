package main

import (
	"io"
	"log"
	"os"
)

func main() {
	path := "/dev/sda"
	log.Println("[+] Reading boot sector of " + path)

	file, err := os.Open(path)
	if err != nil {
		log.Fatal("Error: ", err.Error())
	}

	byteSlice := make([]byte, 512)
	numBytesRead, err := io.ReadFull(file, byteSlice)
	if err != nil {
		log.Fatal("Error reading 512 bytes from file: " + err.Error())
	}

	log.Printf("Bytes read: %d\n\n", numBytesRead)
	log.Printf("Data as decimal:\n%d\n\n", byteSlice)
	log.Printf("Data as hex:\n%x\n\n", byteSlice)
	log.Printf("Data as string:\n%s\n\n", byteSlice)
}
