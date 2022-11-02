# This is a sample Python script.

import datetime


import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

TIMER = 10

node_2_storage = {}


@app.route('/get-data', methods=['POST'])
def receiveTransaction():
    incoming_data = request.values
    transaction_id = incoming_data["id"]
    msg = incoming_data["msg"]
    node_2_storage[transaction_id] = [datetime.datetime.now().timestamp(), msg]

    return jsonify({'tasks': "tasks"})


@app.route('/prepare', methods=['POST'])
def receivePrepare():
    print("received prepare in node2.")
    if datetime.datetime.now().timestamp() - node_2_storage["1"][0] > 15.0:
        print("sending no. ")
        r = requests.post('http://localhost:8080/ack', data={'msg': "NO"})
    else:
        print("sending yes. ")
        r = requests.post('http://localhost:8080/ack', data={'msg': "YES"})

    return str(r.status_code)


@app.route('/commit', methods=['POST'])
def receive_commit():
    data = request.values
    if node_2_storage.get(data["id"]):
        print("this transaction is committed: node2")
    else:
        print("invalid id")

    return "ok"


#
def start_node2():
    app.run(port=8082, debug=False, threaded=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
