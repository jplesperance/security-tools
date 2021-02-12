#!/usr/bin/python3

import socket
import sys
import time
import re
import getopt
from os import path


def main(argv):
    users = ''
    ips = ''
    try:
        opts, args = getopt.getopt(argv, "hi:u:",["ips=","users="])
    except getopt.GetoptError:
        print('smtp-enum.py -i <file> -u <file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('smtp-enum.py -i <file> -u <file>')
            sys.exit()
        elif opt in ("-i", "--ips"):
            ips = arg
        elif opt in ("-u", "--users"):
            users = arg
    if users == '':
        print("A file with a list of usernames must be provided")
        sys.exit(1)
    if ips == '':
        print("A file with a list of host ips must be provided")
        sys.exit(1)
    if not path.exists(users):
        print("File: %s does not exist" % users)
        sys.exit(1)
    if not path.exists(ips):
        print("File: %s does not exist" % users)
    usernames = []
    ipaddys = []
    userfile = open(users, "r")
    for line in userfile:
        user = line.strip("\n")
        users.append(user)

    ipsfile = open(ips, "r")
    for line in ipsfile:
        ip = line.strip("\n")
        ipaddys.append(ip)

    for ip in ipaddys:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, 25))
        banner = s.recv(1024)

        print ""

if __name__ == "__main__":
    main(sys.argv[1:])
