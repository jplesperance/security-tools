package main

import (
	"fmt"
	"log"
	"os"
)

var (
	fileInfo os.FileInfo
	err      error
)

func main() {
	if len(os.Args) != 2 {
		log.Fatal("No file provided")
	}
	file := os.Args[1]
	fileInfo, err = os.Stat(file)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("File Name: ", fileInfo.Name())
	fmt.Println("Size in bytes: ", fileInfo.Size())
	fmt.Println("Permissions: ", fileInfo.Mode())
	fmt.Println("Last Modified: ", fileInfo.ModTime())
	fmt.Println("Is Directory: ", fileInfo.IsDir())
	fmt.Printf("System interface type: %T\n", fileInfo.Sys())
	fmt.Printf("System Info: %+v\n\n", fileInfo.Sys())
}
