# This is a sample Python script.
import datetime
import pickle
import socket
import time
from threading import Thread
import uuid

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

TIMER = 10

request_store = {}

transaction_data = []
global node_count
node_count = 0

commit_id = uuid.uuid4()
transaction_info = {1:commit_id}

def store_transaction_info():
    pass


@app.route('/send-transaction', methods=['GET'])
def sendTransactionDetails():
    r = requests.post('http://localhost:8081/get-data', data={'id': 1, 'msg': 'some-data'})

    r = requests.post('http://localhost:8082/get-data', data={'id': 1, 'msg': 'some-data'})
    request_store[1] = [datetime.datetime.now().timestamp(), ["node1", False], ["node2", False]]
    return str(r.status_code)


@app.route('/send-prepare', methods=['POST'])
def send_prepare():
    data = request.values
    print("Sending prepare message")
    r = requests.post('http://localhost:8082/prepare', data={'id': 1})
    try:
        r = requests.post('http://localhost:8081/prepare', data={'id': 1})
    except:
        print("no response from node 2. aborting transaction")

    return "done"




@app.route('/ack', methods=['POST'])
def receive_prepare_response():
    global node_count
    incoming_data = request.values

    if incoming_data["msg"] == "YES":
        if (datetime.datetime.now().timestamp() - request_store[1][0]) > 20.0:
            print("delay from nodes.. need to abort")
        else:
            node_count += 1
            if node_count == 2:
                print("accept the response from nodes. send commit")
            else:
                print("awaiting ack from other node.")
    else:
        print("aborting transaction.. either node is down or there's delay ")

    return "ok"


global data_loaded
data_loaded = None


@app.route('/commit', methods=['POST'])
def send_commit():
    global data_loaded
    data = request.values
    if data.get("failure") is None:
        r = requests.post('http://localhost:8081/commit', data={'id': 1, 'commit_id':commit_id})
        r = requests.post('http://localhost:8082/commit', data={'id': 1, 'commit_id': commit_id})
        print("Committed transaction to both nodes")
        return "done"

    if data["failure"] == "True":
        request_store[1][1][1] = True
        print("saving to file...", request_store)
        pickle.dump(request_store, open('tc.json', 'wb'))
        r = requests.post('http://localhost:8081/commit', data={'id': 1, 'commit_id':commit_id})
    else:
        print("checking file.")
        data_loaded = pickle.load(open('tc.json', 'rb'))
        if not data_loaded[1][2][1]:
            data_loaded[1][2][1] = True
        print("saving to file...", data_loaded)
        pickle.dump(data_loaded, open('tc.json', 'wb'))
        r = requests.post('http://localhost:8082/commit', data={'id': 1, 'commit_id': commit_id})


    return str("successful")


@app.route('/get-commit-id', methods=['POST'])
def send_commit_to_node():
    data = request.values
    id = data["id"]
    return str(transaction_info[int(id)])



def start_tc(port=None):
    if not port:
        app.run(port=8080, debug=False)
    else:
        app.run(port=port, debug=False)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
