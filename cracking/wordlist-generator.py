import itertools
import click

@click.command()
@click.option('--chars', default='abcdefghijklmenoprstuvwxyz1234567890', help='The charset to use for generation')
@click.option('-o', default='wordlist.txt', help='The output file to write the generated string combinations')
@click.option('--length', default=8, help='The length of the strings to generate')
def generate(chars, o, length):
    chars = split(chars)
    count = 0
    f = open(o, "w")
    for x in permutate(chars, length):
        count +=1
        f.write(''.join(x)+"\n")
    print("[ ] Generated %d string combinations" % count)
    f.close()

def permutate(l, length):
    print("[ ] Generating all possible string combinations at 6 characters long.")
    print("[ ] Using charset: " + str(''.join(l)))
    yield from itertools.product(*([l] * length))
    print("[+] Generation Complete.")

def split(word):
    return [char for char in word]

if __name__ == '__main__':
    generate()

