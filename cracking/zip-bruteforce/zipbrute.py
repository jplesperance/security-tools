#!/usr/bin/env python3
import itertools
import os
import zipfile

import click


@click.group()
def cli():
    pass


def check_zip(zf):
    for zinfo in zf.infolist():
        is_encrypted = zinfo.flag_bits & 0x1
        if is_encrypted:
            return True
        else:
            return False


@click.command('brute', help='Bruteforce attack the encrypted zip file')
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


@click.command('wordlist', help='Generate a wordlist for brutefoce attack')
@click.option('-c', '--chars', default='abcdefghijklmenoprstuvwxyz1234567890', help='The charset to use for generation')
@click.option('-o', '--outfile', default='wordlist.txt', help='The output file to write the generated string combinations')
@click.option('-t', '--type', 'ltype', default='static', type=click.Choice(['static', 'range'], case_sensitive=False), help='Type of password length')
@click.option('-l', '--length', default="8", help="ex. 8 for static, 6:8 for range, format")
def wordlist(chars, outfile, ltype, length):
    chars = split(chars)
    count = 0
    f = open(outfile, "w")
    if ltype == 'static':

        for x in permutate(chars, int(length)):
            count += 1
            f.write(''.join(x) + "\n")
        print("[*] Generated %d string combinations" % count)
        f.close()

    else:
        length = length.split(':')
        for i in range(int(length[0]), int(length[1]) + 1):
            for x in permutate(chars, i):
                count += 1
                f.write(''.join(x) + "\n")

        print("[ ] Generated %d string combinations" % count)
        f.close()


def permutate(l, length):
    print("[*] Generating all possible string combinations at " + str(length) + " characters long.")
    print("[*] Using charset: " + str(''.join(l)))
    yield from itertools.product(*([l] * length))
    print("[+] Generation Complete.")


def split(word):
    return [char for char in word]


if __name__ == '__main__':
    cli.add_command(wordlist)
    cli.add_command(brute)
    cli()
