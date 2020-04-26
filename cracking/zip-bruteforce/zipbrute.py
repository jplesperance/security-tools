#!/usr/bin/env python3

import os
import zipfile

import click


def check_zip(zf):
    for zinfo in zf.infolist():
        is_encrypted = zinfo.flag_bits & 0x1
        if is_encrypted:
            return True
        else:
            return False


@click.command(help='Bruteforce attack the encrypted zip file')
@click.option('-p', '--password', type=click.types.STRING, help='Password for encrypted zip file')
@click.option('-w', '--wordlist', type=click.types.STRING, help='Wordlist to use for encrypted zip file')
@click.argument('file', default='archive.zip')
def brute(password, wordlist, file):
    if not os.path.isfile(file):
        print("[-] The specified zip file does not exist: ", file)
        exit(1)

    if wordlist:
        if not os.path.isfile(wordlist):
            print("[-] The specified wordlist could not be found")
            exit(1)

    if not password and not wordlist:
        print("[-] A password or wordlist mush be specified")
        exit(1)

    zf = zipfile.ZipFile(file, 'r')
    cracked = False
    if check_zip(zf):
        if not password:
            with open(wordlist) as f:
                lines = f.readlines()
                for p in lines:
                    p = str(p.replace("\n", ""))

                    try:
                        zf.extractall(pwd=bytes(p, 'utf-8'))
                        print("[+] Password Found: " + p)
                        cracked = True
                    except:
                        pass

        else:
            try:
                zf.extractall(pwd=bytes(password, 'utf-8'))
                print("[+] Password Found: " + password)
                cracked = True
            except:
                pass

        if not cracked:
            print("[-] Password Not Found!")
    else:
        print('[*] Zip file is not encrypted, bruteforcing not required')
        exit(0)

    print('[+] Done!')





if __name__ == '__main__':
    brute()
