# This is a sample Python script.
import datetime
import pickle
import socket
import time
from threading import Thread

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

TIMER = 10

node_1_storage = {}


@app.route('/get-data', methods=['POST'])
def receiveTransaction():
    incoming_data = request.values
    transaction_id = incoming_data["id"]
    msg = incoming_data["msg"]
    node_1_storage[transaction_id] = [datetime.datetime.now().timestamp(), msg]
    return jsonify({'tasks': "tasks"})


@app.route('/prepare', methods=['POST'])
def receivePrepare():
    print("received prepare in node1.",datetime.datetime.now().timestamp() - node_1_storage["1"][0])
    if datetime.datetime.now().timestamp() - node_1_storage["1"][0] > 15.0:
        print("sending no. ")
        r = requests.post('http://localhost:8080/ack', data={'msg': "NO"})
    else:
        print("sending yes. ")
        pickle.dump({"id":"1"}, open('node1.json', 'wb'))
        r = requests.post('http://localhost:8080/ack', data={'msg': "YES"})

    return str(r.status_code)

@app.route('/commit', methods=['POST'])
def receive_commit():
    data = request.values
    if node_1_storage.get(data["id"]):
        print("this transaction is committed => Node1")
    else:
        print("invalid id")

    return "ok"

@app.route('/get-commit-from-tc', methods=['POST'])
def get_commit():
    data_loaded = pickle.load(open('node1.json', 'rb'))

    r = requests.post('http://localhost:8080/get-commit-id', data=data_loaded)
    print("commiting the transaction for id 1 with commit_id",id, r.content)
    return "ok"

def start_node1():
    print("starting node 1...")
    app.run(port=8081, debug=False, threaded=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
