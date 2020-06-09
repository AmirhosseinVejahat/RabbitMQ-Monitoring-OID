#!/usr/bin/python
import requests
from requests.auth import HTTPBasicAuth
from pprint import pprint
import json
import pyagentx


USERNAME = "guest"
PASSWORD = "guest"
HOST = "http://127.0.0.1:15672"


def send_request(url):
    
    resp = requests.get(url,auth=HTTPBasicAuth(USERNAME,PASSWORD))
    resp = resp.json()
    return resp

def overview():

    url = HOST + "/api/overview"
    resp = send_request(url)
    return resp

def total_connections():

    resp = overview()
    return resp["object_totals"]["connections"]

def consumer_exists():

    resp = overview()
    if resp["object_totals"]["consumers"] > 0:
        return 1
    return 0

def publish_rate():

    resp = overview()
    return resp["message_stats"]["publish_details"]["rate"]

def total_published_message():

    resp = overview()
    return resp["message_stats"]["publish"]

def consume_rate():

    resp = overview()
    return resp["message_stats"]["deliver_get_details"]["rate"]


def total_consumed_message():

    resp = overview()
    return resp["message_stats"]["deliver_get"]


def check_queue_exists(queue='uequeue'):

    url = HOST + "/api/queues"
    resp = send_request(url)
    for q in resp:
        if q["name"] == queue:
            return 1
    return 0

def queue_size():

    url = HOST + '/api/queues/%2F/uequeue'
    resp = send_request(url)
    return resp["messages"]


def check_aliveness():

    url = HOST + "/api/aliveness-test/%2F"
    resp = send_request(url)
    if resp["status"] == "ok":
        return 1
    return 0


def node_status():

    url = HOST + "/api/nodes/1"
    resp = send_request(url)
    return resp


class Snmp(pyagentx.Updater):
    def update(self):
        self.set_INTEGER('1.0',check_aliveness())
        self.set_INTEGER('2.0',check_queue_exists())
        self.set_INTEGER('3.0',total_consumed_message())
        self.set_INTEGER('4.0',total_published_message())
        self.set_OCTETSTRING('5.0',str(publish_rate()))
        self.set_OCTETSTRING('6.0',str(consume_rate()))
        self.set_INTEGER('7.0',total_connections())
        self.set_INTEGER('8.0',queue_size())

class MyAgent(pyagentx.Agent):
    def setup(self):
        self.register('1.3.6.1.4.1.8072.1234.1234',Snmp)



if __name__ == '__main__':

    pyagentx.setup_logging()
    try:
        a = MyAgent()
        a.start()
    except Exception as e:
        print("Unhandled exception",e)
        a.stop()
    except KeyboardInterrupt:
        a.stop()
