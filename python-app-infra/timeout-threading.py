import threading
import time
import random
import heapq
import sys,signal

class TimerIntf():
    def run():
        pass

class myObj(TimerIntf):
    def __init__(self, name):
        self.name = "Timer-" + str(name)
    def run(self, to):
        print self.name , " My timer expired @ run() ", to

# Can also make this singleton
class myTimeout(object):
    _shared = None
    def __new__(cls):
        if not cls._shared:
            cls._shared = object.__new__(cls,myTimeout)
        return cls._shared
        
    def __init__(self):
        self.q = []
        self.evt = threading.Event()
        self.qlock = threading.Lock()
        self.evtThr = threading.Thread(target=self.waitEvent)
        self.evtThr.daemon = True
        self.evtThr.start()

    # 'to' in seconds
    def callAfterTimeoutSecs(self,to, obj):
        tc = to + time.time()
        self.qlock.acquire()
        heapq.heappush(self.q, (tc, obj))
        self.qlock.release()
        print "(qlen %d) "% len(self.q),' timeout ',to, '({})'.format(tc)
        self.evt.set()
    
    def waitEvent(self):
        while True:
            tw = None
            self.qlock.acquire()
            if self.q:
                (to,obj) = heapq.heappop(self.q)
                tw = to - time.time()
            self.qlock.release()
            #print "Event Wait ", tw, to if tw else None
            rc = self.evt.wait(tw)
            if rc == False: # no event occurred (instead timeout happened)
                obj.run(to)
            else:
                self.evt.clear()
                if tw: heapq.heappush(self.q, (to,obj))
            
def inthandler(signum, frame):
    print "Exiting ..."
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, inthandler)
    t = myTimeout()
    MAXTIME,NEVT=10,5
    
    for i in range(NEVT):
        ti = random.randint(1,MAXTIME)
        obj = myObj(i+100)

        # Insert a time to wait with TimerIntf Object
        t.callAfterTimeoutSecs(ti,obj)

    time.sleep(MAXTIME)
