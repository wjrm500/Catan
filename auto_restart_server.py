from shutil import which
import subprocess
from time import sleep

def is_tool(name):
    return which(name) is not None

def start_script():
    try:
        if is_tool('python3.9'):
            subprocess.run('python3.9 server.py', shell = True)
        else:
            subprocess.run('python server.py', shell = True)
    except Exception as ex:
        handle_crash(ex)

def handle_crash(ex):
    print(ex)
    sleep(2)
    start_script()

start_script()