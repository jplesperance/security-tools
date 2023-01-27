#!/bin/python3

import os
import sys

def main(argv):
    octet = sys.argv[1]
    first = int(sys.argv[2])
    last = int(sys.argv[3])
    ip = ''
    for i in range(first, last+1):
        ip = octet +"." + str(i)
        resp = os.system("ping -c 1 -w 1 " + ip + " >/dev/null")
        if resp == 0:
            print(ip)
if __name__ == "__main__":
    main(sys.argv)
