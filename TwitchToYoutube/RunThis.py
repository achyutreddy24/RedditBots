#!/usr/bin/env python3
import time
import subprocess
WAIT = 30
while True:
    try:
        subprocess.call("python main.py", shell=True)
    except Exception as e:
        print("ERROR:", str(e))
    print('Sleeping ' + str(WAIT) + ' seconds.\n')
    time.sleep(WAIT)
