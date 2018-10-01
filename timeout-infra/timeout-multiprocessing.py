#!/bin/env python
#
# Simple timer utility
#

from multiprocessing import *
import time
import random
import heapq
import os,sys
import signal
import constant

class TimerIntf(object):
    def run(self): pass
        
class myObj(TimerIntf):
    def __init__(self, name):
        self.name = "Timer-" + str(name)
    def run(self, to):
        print self.name , " My timer expired @ run() ", to

class myTimeout(object):
    _shared = None
    def __new__(cls):
        if not cls._shared:
            cls._shared = object.__new__(cls,myTimeout)
        return cls._shared

    def __init__(self):
        self.seqno = 1 # Next available seqno.
        self.evt = Event()
        self.qlock = Lock()
        self.cancelq, self.q = Manager().list(), Manager().list()
        self.p = Process(target=self.mainEventLoop, args=(self.evt,self.q,self.qlock,self.cancelq,))
        self.p.start()

    def do_cancel(self,lq,cq):
        # got cancel notification
        cl = []
        if not cq: return
        self.qlock.acquire()
        while cq:
            cl.append(cq.pop())
        self.qlock.release()
        for v in cl:
          for i in list(lq):
            if i[1]._id == v:
                print '   (timer removed ', v, ')'
                lq.remove((i))
                heapq.heapify(lq)

        
    def mainEventLoop(self,evt,q,qlock,cq):
        lq = []
        while True:
            tw = None
            qlock.acquire()
            while q:
                i = q.pop()
                heapq.heappush(lq,(i[0],i[1]))
            qlock.release()

            self.do_cancel(lq,cq)

            if lq:
                (to,obj) = heapq.heappop(lq)
                tw = to - time.time()

            rc = evt.wait(tw)
            if rc == False:
                obj.run(to)
            else:
                evt.clear()
                if tw: 
                    heapq.heappush(lq, (to,obj))

    # Returns TimerHandle object
    def callAfterTimeoutSecs(self, to, obj):
        tc = to + time.time()
        obj._tc = tc
        obj._id = self.seqno
        self.qlock.acquire()
        self.q.append((tc,obj))
        self.qlock.release()
        self.seqno += 1
        self.evt.set()
        return obj

    # Timeout fn() will not be executed after this call
    def cancelPendingTimeout(self, th):
        self.qlock.acquire()
        self.cancelq.append(th._id)
        self.qlock.release()
        self.evt.set()
        return
        

def inthandler(signum, frame):
    print "User Terminated. Exiting ...", current_process().pid, current_process().name
    sys.exit(0)

if __name__ == "__main__":
    thlist = []
    print 'Testing Timer Infra (time=',time.time(),')'
    constant.nT = 25
    constant.tRange = [10,30]

    signal.signal(signal.SIGINT, inthandler)
    t = myTimeout()
    # Create bunch of test timers
    for i in range(1,constant.nT):
        ti = random.randint(*constant.tRange)
        obj = myObj(i+100)

        # Insert a time to wait with TimerIntf Object
        th = t.callAfterTimeoutSecs(ti,obj)
        thlist.append(th)
        print ' Creating ', i, ' timer ', th.name, ' fires after ', ti, ' secs @ ', th._tc

    time.sleep(random.randint(1,3))
    rl = random.sample(thlist, constant.nT/2)
    for i in rl:
        # Pick a timer index and cancel
        print i.name,' Cancelling ', i._id, ' timer @ ', i._tc
        t.cancelPendingTimeout(i)

    #evtThr.join() # Blocking to signals
    while True: time.sleep(100)
