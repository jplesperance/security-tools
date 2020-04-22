#!/usr/bin/python

import sys
import binascii
import re
import os

from subprocess import Popen, PIPE

def dict_size(dictionary):
    lines = 0
    with open(dictionary) as f:
        for line in f:
            if len(re.sub(r'\W', '', line)) == 5:
                lines += 1
    return lines

if len(sys.argv) < 3:
    print("Usage: ./autowep.py <wordlist> <pcap_file>")
    exit(0)

wordlist = sys.argv[1]
if not os.path.isfile(wordlist):
    print("The specified wordlist cannot be found: ", wordlist)
    exit(1)

pcapFile = sys.argv[2]
if not os.path.isfile(pcapFile):
    print("The pcap file specified does not exist: ", pcapFile)
    exit(1)

f = open(wordlist, 'r')
print("Loaded "+ str(dict_size(wordlist)) + " words")

for line in f:
    wepKey = re.sub(r'\W+', '', line)
    if len(wepKey) != 5:
        continue

    hexKey = binascii.hexlify(wepKey)
    p = Popen(['/usr/bin/airdecap-ng', '-w', hexKey, pcapFile], stdout=PIPE)
    output = p.stdout.read()
    finalResult = output.split("\n")[4]
    if finalResult.find('1') != -1:
        print("[SUCCESS]: WEP Key found: ", wepKey)
        sys.exit(0)
print("[FAIL]: WEP Key could not be found using the specified wordlist")
