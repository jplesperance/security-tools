import itertools

import click


@click.command()
@click.option('--chars', default='abcdefghijklmenoprstuvwxyz1234567890', help='The charset to use for generation')
@click.option('-o', default='wordlist.txt', help='The output file to write the generated string combinations')
@click.option('--length-type', default='static', type=click.Choice(['static', 'range'], case_sensitive=False))
@click.option('--length', default="8", help="ex. 8 for static, 6:8 for range, format")
def generate(chars, o, length_type, length):
    chars = split(chars)
    count = 0
    f = open(o, "w")
    if length_type == 'static':

        for x in permutate(chars, int(length)):
            count += 1
            f.write(''.join(x) + "\n")
        print("[*] Generated %d string combinations" % count)
        f.close()

    else:
        length = length.split(':')
        for i in range(int(length[0]), int(length[1])+1):
            for x in permutate(chars, i):
                count += 1
                f.write(''.join(x) + "\n")

        print("[ ] Generated %d string combinations" % count)
        f.close()


def permutate(l, length):
    print("[*] Generating all possible string combinations at "+str(length)+" characters long.")
    print("[*] Using charset: " + str(''.join(l)))
    yield from itertools.product(*([l] * length))
    print("[+] Generation Complete.")


def split(word):
    return [char for char in word]


if __name__ == '__main__':
    generate()

