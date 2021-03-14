#!/bin/env python3
#
# Author: Shankar, K
# Date: Dec 2018
#
# Description: Simple Microservice which monitors the Health of SDX
# and publishes the health over the 'RabbitMQ' message broker
#

import multiprocessing as mp
import time
from time import sleep
import sys,os
import telnetlib
import re
from nameko.standalone.events import event_dispatcher
from nameko.events import EventDispatcher
from nameko.rpc import rpc
import redis

"""
This Service determines the health of Known SDXs

State:
    1. NAV: not present  (not given)
    2. PEN: pending      (currently under test)
    3. RDY: PingReady    (SSH Ready?)
    4. NOK: PingFailed   (SSH Failed?)

Additional Properties
    
    5. lastpingtime
    6. lastpingsuccesstime
    7. lastchecked
    8. lastchecksuccess

"""

def try_login(tn,to):
    tn.write("\n".encode('ascii'))
    alist = [ b'login: ', b'\]\# $', b'1 - Initiate a regular session' ]
    [ a,b,st ] = tn.expect(alist, to)
    print('a ',a,'b ',b,'st ',st)
    match = re.search(rb'.*1 - Initiate.*', st)
    if match:
        tn.write("1\n".encode('ascii'))
        alist = [ b'login: ', b'\]\# $' ]
        [ a,b,st ] = tn.expect(alist, to)
    return True if a!=-1 else False

def do_poll_sdx(tn, initial, interval, count,to):
    print("\nWaiting for sdx system to come up\n")
    time.sleep(initial) # Wait for system to go down
    cnt=count
    trytime=interval
    while(cnt > 0):
        m = try_login(tn,to)
        if m: return 0
        time.sleep(trytime)
        cnt -= 1
        print("trying sdx (if its up)...")
    # If it comes here, sdx is not up
    raise "SDX is not up. Aborting"

class SDXHealth(object):
    name = "SDXHealth"
    _redis = None
    _dispatch = None

    _redis = redis.StrictRedis()
    CONFIG={"AMQP_URI" : "amqp://guest:guest@localhost"}
    _dispatch = EventDispatcher()

    #def __init__(self,sdx): self.sdx = sdx

    # Returns True if Successful, False If not
    def ConsoleHealth(self, sdx):
        to,rc = 15, True
        cip,cport = sdx["Console IP"], sdx["Console Port"]
        try:
            tn = telnetlib.Telnet(cip,cport, to)
            do_poll_sdx(tn, 0, 30, 2,to)
        except Exception as e:
            rc = False
            print (e)
        ts = time.time()
        key = cip + '_'+ str(cport)
        value = { 'id':key,'state':'RDY', 'lastchecked':ts,'lastchecksuccess':ts} if rc else {'state':'NOK', 'lastchecked':ts,'lastchecksuccess':None, 'id':key}
        # put it in redis
        #if self._redis.exists(key): self._redis.delete(key)
        self._redis.hmset(key, value)

        # publish to nameko
        self._dispatch("consolehealth", str(value))
        return
    
    def DOM0Ip(self, sdx):
        cip,cport = sdx["Console IP"], sdx["Console Port"]
        ip = sdx["DOM0 Mgmt IP"]
        rc = os.system("ping -c 1 " +  ip)
        ts = time.time()
        key = cip + '_'+ str(cport)
        value = {'pingstate':'NOK', 'pinglastchecked':ts,'pinglastchecksuccess':None, 'id':key, 'pingip': ip } if rc != 0 else { 'id':key,'pingstate':'RDY', 'pinglastchecked':ts,'pinglastchecksuccess':ts , 'pingip': ip }
        # put it in redis
        #if self._redis.exists(key): self._redis.delete(key)
        self._redis.hmset(key, value)

        # publish to nameko
        self._dispatch("pinghealth", str(value))
        return 
        
    def LOMIp(self): pass

    @rpc
    def Run(self, sdx):
        print ("Run Called ", sdx, self._dispatch, self._redis)
        self.ConsoleHealth(eval(sdx))
        self.DOM0Ip(eval(sdx))
        #a = mp.Process(target=self.ConsoleHealth, args=(eval(sdx),))
        #a.start()

