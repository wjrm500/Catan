from shutil import which
import subprocess
from time import sleep

def is_tool(name):
    return which(name) is not None

def start_script():
    try:
        if is_tool('python3.9'):
            subprocess.run(f'python3.9 server.py')
        else:
            subprocess.run(f'python server.py')
    except Exception as e:
        handle_crash(e)

def handle_crash(e):
    print(e.message)
    sleep(2)
    start_script()

start_script()