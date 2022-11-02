import threading
import time
import requests
from threading import Thread
import multiprocessing
import node1
import node2
import tc


import ctypes

def kill_thread(thread):
    """
    thread: a threading.Thread object
    """
    thread_id = thread.ident
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
    if res > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
        print('Exception raise failure')

if __name__ == '__main__':
    t3 = Thread(target=node2.start_node2)
    t3.start()

    time.sleep(3)
    while True:
        print("case 1. TC goes down before sending prepare.")
        print("case 2 Simulating node failure, node does not send ack with YES / no to tc")
        print("case 3 happy case.")
        print("case 4: tc reads info from file to send commit info")
        print("case 5: Node reads info from file to get transaction id and fetches commit id from tc")

        val = input("Enter your action: ")

        if str(val) == "1":
            t1 = multiprocessing.Process(target=tc.start_tc)
            t2 = multiprocessing.Process(target=node1.start_node1)
            t1.start()
            t2.start()
            time.sleep(0.1)
            r = requests.get('http://localhost:8080/send-transaction')
            print("simulating tc failure now.")
            # t1.terminate()
            # t1 = multiprocessing.Process(target=tc.start_tc)
            # t1.start()
            time.sleep(15)
            rr = requests.post('http://localhost:8080/send-prepare')

            t1.terminate()
            t2.terminate()
        elif str(val) =="2":
            t1 = multiprocessing.Process(target=tc.start_tc)
            t2 = multiprocessing.Process(target=node1.start_node1)
            t1.start()
            t2.start()
            time.sleep(0.1)
            r = requests.get('http://localhost:8080/send-transaction')
            print("simulating node failure now.")
            t2.terminate()
            time.sleep(2)
            rr = requests.post('http://localhost:8080/send-prepare')
            t1.terminate()
        elif str(val) == "3":
            t1 = multiprocessing.Process(target=tc.start_tc)
            t2 = multiprocessing.Process(target=node1.start_node1)
            t1.start()
            t2.start()

            r = requests.get('http://localhost:8080/send-transaction')
            print("simulating prepare")
            rr = requests.post('http://localhost:8080/send-prepare')
            print("initiating commit.")
            requests.post('http://localhost:8080/commit', data={})

            t1.terminate()
            t2.terminate()

        elif str(val) =="4":
            t1 = multiprocessing.Process(target=tc.start_tc)
            t2 = multiprocessing.Process(target=node1.start_node1)
            t1.start()
            t2.start()
            time.sleep(0.1)
            r = requests.get('http://localhost:8080/send-transaction')
            rr = requests.post('http://localhost:8080/send-prepare')

            print("initiating commit to both nodes.")
            requests.post('http://localhost:8080/commit', data={'failure': "True"})
            print("TC server crashes..")
            print("restarting tc")
            t1.terminate()
            t1 = multiprocessing.Process(target=tc.start_tc)
            t1.start()
            time.sleep(0.5)
            requests.post('http://localhost:8080/commit', data={'failure': "False"})
            t1.terminate()
            t2.terminate()
        elif str(val) == "5":
            t1 = multiprocessing.Process(target=tc.start_tc)
            t2 = multiprocessing.Process(target=node1.start_node1)
            t1.start()
            t2.start()
            time.sleep(0.1)
            r = requests.get('http://localhost:8080/send-transaction')
            rr = requests.post('http://localhost:8080/send-prepare')
            t2.terminate()
            time.sleep(5)
            t2 = multiprocessing.Process(target=node1.start_node1)
            t2.start()
            print("getting commit")
            requests.post('http://localhost:8081/get-commit-from-tc', data={'id': "1"})












