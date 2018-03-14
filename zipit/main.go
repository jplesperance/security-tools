package main

import (
	"archive/zip"
	"crypto/md5"
	"crypto/sha1"
	"crypto/sha256"
	"crypto/sha512"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"os"
)

func printUsage() {
	fmt.Println("Usage: ", os.Args[0], " <filepath>")
	fmt.Println("Example: ", os.Args[0], " document.txt")
}

func checkArgs() string {
	if len(os.Args) < 2 {
		printUsage()
		os.Exit(1)
	}
	return os.Args[1]
}

func ZipFiles(filename string, files []string) error {
	newFile, err := os.Create(filename)
	if err != nil {
		return err
	}
	defer newFile.Close()

	zipWriter := zip.NewWriter(newFile)
	defer zipWriter.Close()

	for _, file := range files {
		zipfile, err := os.Open(file)
		if err != nil {
			return err
		}
		defer zipfile.Close()

		info, err := zipfile.Stat()
		if err != nil {
			return err
		}

		header, err := zip.FileInfoHeader(info)
		if err != nil {
			return err
		}

		header.Method = zip.Deflate

		writer, err := zipWriter.CreateHeader(header)
		if err != nil {
			return err
		}

		_, err = io.Copy(writer, zipfile)
		if err != nil {
			return err
		}
	}
	return nil
}

func main() {
	filename := checkArgs()
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		log.Fatal(err.Error())
	}

	files := []string{filename}
	output := "test.zip"

	err = ZipFiles(output, files)

	if err != nil {

		log.Fatal(err.Error())
	}

	fmt.Printf("Zipped File: %s \n\n", output)
	fmt.Printf("MD5: %x\n\n", md5.Sum(data))
	fmt.Printf("SHA1: %x\n\n", sha1.Sum(data))
	fmt.Printf("SHA256: %x\n\n", sha256.Sum256(data))
	fmt.Printf("SHA512: %x\n\n", sha512.Sum512(data))
}
