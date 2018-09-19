import ctypes as c
import signal
import os, sys
import time
import threading

class ProcessEvent(object):
    def __init__(self):
        # Initialize library
        libname = os.path.abspath(os.path.join(os.path.dirname(__file__), "libpmon.so"))
        self.plib = c.CDLL(libname)

    def registerCB(self, cb):
        # Register callback to be called for every process event
        cb_proto = c.CFUNCTYPE(None, c.c_int, c.c_void_p)
        ccb = cb_proto(cb) # ccb can be used as normal 'c' argument
        self.plib.register_cb(ccb)

    def start(self):
        # start the monitoring service
        self.plib.handle()

    def stop(self):
        # stop the monitoring service
        self.plib.stop()

class pedata(c.Structure):
    _fields_ = [ ('x', c.c_int), ('y',c.c_int), ('a', c.c_int), ('b', c.c_int) ]


def recvevent(evt, buf):
    pev = c.cast(buf, c.POINTER(pedata)).contents

    # General Processing - Sample shown below
    PROC_EXIT=-2147483648
    PROC_FORK=1
    PROC_EXEC=2
    EVT = {PROC_EXIT: 'EXIT', PROC_FORK:'FORK',PROC_EXEC:'EXEC'}
    ph = {}
    print "Callback ",EVT[evt] if evt in EVT else evt , pev.x, pev.y, pev.a, pev.b
    if evt == PROC_EXIT:
        if pev.x in ph:
            ph[pev.x] -= 1
    elif evt == PROC_FORK:
        ph[pev.x] = ph.setdefault(pev.x, 1)
        ph[pev.a] = ph.setdefault(pev.x, 1)
    #elif evt == PROC_EXEC: pass
    else:
        pass

def inthandler(c,f):
    if evt: evt.stop()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, inthandler)
    evt = ProcessEvent()
    evt.registerCB(recvevent)
    t = threading.Thread(target=evt.start)
    t.daemon = True
    t.start()

    while True:
        time.sleep(10)

    t.join()
