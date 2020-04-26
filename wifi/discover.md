## Usage ##

This tool is designed to monitor wireless network traffic.  Various arguments can be passed to the tool to customize what type of data it captures.

### Running the tool:
    
While there are several different arguments that can be used with `discover`, requires at least one of the following arguments to be provided: -k -h -p -d
    
    ./discover.py -k

### Typical Usage Examples:

Capture only broadcasted SSIDs

    ./discover -k
    
Capture only hidden networks
    
    ./discover -h
    
Capture the SSID for hidden networks

    ./discover -d
    
Capture broadcasted and hidden networks.  Use association responses to find the SSID for hidden networks

    ./discover -k -h -d

### Options

Find and log broadcasted networks

    -k, --known
    
Find and log hidden networks

    -h, --hidden

Log Client Probes(none, all probes, probes for unknown networks) for SSIDs

    -p, --probes [none|unknown|all] - default to none
    
Find and log SSIDs for hidden networks using association response packets

    -d, --discover-hidden
    
Define the interface to use, must be in monitor mode

    -i, --interface <iface>
Define what to prepend the output filenames with
    
    -w, --write <file>
How long to run the scan

    -t, --time <int>
       
