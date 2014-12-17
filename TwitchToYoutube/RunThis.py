import time
import subprocess
WAIT = 30
while True:
    try:
        subprocess.call("python main.py")
    except Exception as e:
        print("ERROR:", e)
    print('Sleeping ' + str(WAIT) + ' seconds.\n')
    time.sleep(WAIT)