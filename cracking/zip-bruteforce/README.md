## Usage ##

Running the tool:
    
    ./zipbrute.py [command] [options]

Typical Usage Examples:

    ./zipbrute.py wordlist -c abcdef123 -t static -l 8 -o wordlist.txt

    ./zipbrute.py brute -w wordlist.txt encrypted.zip

Options:

    wordlist -- Usage: zipbrute.py [OPTIONS]

        -c abc, --chars=abc                      the charset to use for wordlist generation

        -t static, --type=static [static|range]  the type of length being specified

        -l 8, --length 6:8                       length(s) of the words in the wordlist to generate, ex. 8 for static or 6:8 for range

        -o file, --outfile file                  the file name output the wordlist to
    
    brute  -- Usage: zipbrute.py brute [OPTIONS] [FILE]
       
        -p password, --password=password            Password for encrypted file
        
        -w wordlist.txt, --wordlist=wordlist.txt    Wordlist to use for bruteforcing encrypted zip file
