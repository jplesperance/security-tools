## Usage ##

Running the tool:
    
    ./wordlist-gen.py [options]

Typical Usage Examples:

    ./wordlist-gen.py -c abcdef123 -t static -l 8 -o wordlist.txt

Options:

    Usage: wordlist-gen.py [OPTIONS]

        -c abc, --chars=abc                      the charset to use for wordlist generation

        -t static, --type=static [static|range]  the type of length being specified

        -l 8, --length 6:8                       length(s) of the words in the wordlist to generate, ex. 8 for static or 6:8 for range

        -o file, --outfile file                  the file name output the wordlist to
