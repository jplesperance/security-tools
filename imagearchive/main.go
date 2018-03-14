package main

import (
	"io"
	"log"
	"os"
)

func main() {
	firstFile, err := os.Open("test.jpg")
	if err != nil {
		log.Fata(err)
	}
	defer firstFile.Close()

	secondFile, err := os.Open("test.zip")
	if err != nil {
		log.Fata(err)
	}
	defer secondFile.Close()

	newFile, err := os.Create("stego_image.jpg")
	if err != nil {
		log.Fatal(err)
	}
	defer newFile.Close()

	_, err = io.Copy(newFile, firstFile)
	if err != nil {
		log.Fatal(err)
	}
	_, err = io.Copy(newFile, secondFile)
	if err != nil {
		log.Fatal(err)
	}
}
