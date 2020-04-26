# Wep Brute Force Script

This script was created to help automate the process for trying to brute force a WEP key in circumstances where you do not have enough weak IVs in you capture file.

## Usage ##

The script only expects 2 parameters, the wordlist to use in the brute force attack and the capture file.  
Running the tool:
    
    ./autowep.py [options] PCAPFILE

Typical Usage Examples:

    ./autowep.py -w wordlist.txt wep.pcap

Options:

    -w wordlist, --wordlist=wordlist.txt        The wordlist to use for brute forcing the WEP key
       
