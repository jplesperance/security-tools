package main

import (
	"bufio"
	"bytes"
	"log"
	"os"
)

func main() {
	filename := "stego_image.jpg"
	file, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}

	bufferedReader := bufio.NewReader(file)

	fileStat, _ := file.Stat()
	for i := int64(0); i < fileStat.Size(); i++ {
		myByte, err := bufferedReader.ReadByte()
		if err != nil {
			log.Fatal(err)
		}

		if myByte == '\x50' {
			byteSlice := make([]byte, 3)
			byteSlice, err = bufferedReader.Peek(3)
			if err != nil {
				log.Fatal(err)
			}

			if bytes.Equal(byteSlice, []byte{'\x4b', '\x03', '\x04'}) {
				log.Printf("Found zip signature at byte %d", i)
			}
		}
	}
}
