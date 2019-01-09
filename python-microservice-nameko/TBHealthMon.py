#!/bin/env python3

import os,sys
import yaml
import uuid
import re
from nameko.events import event_handler
from nameko.standalone.rpc import ClusterRpcProxy

sys.path.insert(0,os.path.dirname(os.path.realpath(__file__))) #Location of ssh_hop

#
# nameko service
#
class TBHealthMon(object):
    name = "TBHealthMon"

    @event_handler("SDXHealth", "pinghealth")
    def handle_ping(self, payload):
        print ("Received Ping: ", payload)
        dh = eval(payload)

    @event_handler("SDXHealth", "consolehealth")
    def handle_console(self, payload):
        print ("Received : ", payload)
        dh = eval(payload)


#
# test code to exercise rpc like a non-nameko client
#
dbdir = "/media/sdxlab/"
nw =  len(os.listdir(dbdir))
for f in os.listdir(dbdir):
    if not re.match(r'.*Ball*', f): continue
    with open(dbdir+f, 'r') as s:
        try:
            appliance = yaml.load(s)
            #dr = SDXHealth(appliance)
            #print(appliance['Device Name'],appliance['Console IP'],appliance['Console Port'])
            #dr.Run() # Async Call for health. Could be RPC call.
            CONFIG={"AMQP_URI" : "amqp://guest:guest@localhost", "max_workers": nw}
            with ClusterRpcProxy(CONFIG) as proxy:
                print ("Coming here")
                proxy.SDXHealth.Run.call_async(str(appliance))

        except yaml.YAMLError as exc:
            print(exc)

