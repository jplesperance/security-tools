#!/usr/bin/env python3

import sys
import binascii
import re
import os
import click

from subprocess import Popen, PIPE


def dict_size(dictionary):
    lines = 0
    with open(dictionary) as f:
        for line in f:
            lines += 1
    return lines


@click.command(help='Brute force the WEP key on a capture file without enough IVs')
@click.option('-w', '--wordlist', 'wordlist', type=click.types.STRING, help='wordlist to use for bruteforce')
@click.argument('pcapfile', type=click.STRING)
def brute(wordlist, pcapfile):

    if not os.path.isfile(wordlist):
        print("The specified wordlist cannot be found: ", wordlist)
        exit(1)

    if not os.path.isfile(pcapfile):
        print("The pcap file specified does not exist: ", pcapfile)
        exit(1)

    f = open(wordlist, 'r')
    print("Loaded " + str(dict_size(wordlist)) + " words")

    for line in f:
        wepKey = re.sub(r'\W+', '', line)
        if len(wepKey) != 5:
            continue

        hexKey = binascii.hexlify(wepKey)
        p = Popen(['/usr/bin/airdecap-ng', '-w', hexKey, pcapfile], stdout=PIPE)
        output = p.stdout.read()
        finalResult = output.split("\n")[4]
        if finalResult.find('1') != -1:
            print("[SUCCESS]: WEP Key found: ", wepKey)
            sys.exit(0)
    print("[FAIL]: WEP Key could not be found using the specified wordlist")


if __name__ == '__main__':
    brute()
