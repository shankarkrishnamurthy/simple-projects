#!/bin/env python3

import os,sys
import yaml
import uuid
import re
from nameko.events import event_handler
from nameko.standalone.rpc import ClusterRpcProxy

sys.path.insert(0,os.path.dirname(os.path.realpath(__file__))) #Location of ssh_hop
#from SDXHealth import SDXHealth

class TBHealthMon(object):
    name = "TBHealthMon"
    @event_handler("TBHealth", "consolehealth")
    def handle(self, payload):
        print ("Received Notification: ", payload)
        dh = eval(payload)
        print ("State ", dh['state'])

dbdir = "/media/sdxlab/"
for f in os.listdir(dbdir):
    if not re.match(r'.*Ball*', f): continue
    with open(dbdir+f, 'r') as s:
        try:
            appliance = yaml.load(s)
            #dr = SDXHealth(appliance)
            #print(appliance['Device Name'],appliance['Console IP'],appliance['Console Port'])
            #dr.Run() # Async Call for health. Could be RPC call.
            CONFIG={"AMQP_URI" : "amqp://guest:guest@localhost"}
            with ClusterRpcProxy(CONFIG) as proxy:
                print ("Coming here")
                proxy.SDXHealth.Run(str(appliance))

        except yaml.YAMLError as exc:
            print(exc)

