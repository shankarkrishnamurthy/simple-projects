#!/bin/env python

# Examples:
#   ./gfunccount.py -s tim -c 'dd if=/dev/zero of=dev/null' -e
#   ./gfunccount -c 'ping www.nitt.edu -c 1' -e
#   ./gfunccount.py -s avg -c 'brctl show'  -e
#   ./gfunccount -s tim -e
#   ./gfunccount --exclusive                    # in order to create exclusive fn(), a front
                                                # room of 1s is given to exclude those functions
                                                # before recording actual functions
#   ./gfunccount --duration  3                  # default: 10 seconds
#   ./gfunccount --interval .1                  # interval between 2 samples (default: 1s)
#   ./gfunccount --sort {hit,time,avg,s2}       # default: hit
#
# Source :
#       head /sys/kernel/debug/tracing/trace_stat/function0 
  #Function                               Hit    Time            Avg             s^2
  #--------                               ---    ----            ---             ---
  #schedule                               212    299295844 us     1411772 us      183116351 us 
  #do_syscall_64                          283    121131849 us     428027.7 us     215357344 us 
#

import os,sys
import multiprocessing
import time
import optparse
import re
import signal

class gfunccount:
    def __init__(self):
        os.system("mount -t debugfs none /sys/kernel/debug/ 2>/dev/null")
        signal.signal(signal.SIGINT, self.sighand)
        parser = optparse.OptionParser()
        parser.add_option('-d','--duration', help="duration of capture" )
        parser.add_option('-c','--cpu', action="append", help="functions only on this cpu")
        parser.add_option('-s','--sort', help="hit/tim/avg")
        parser.add_option('-e','--exclusive',default=False, action="store_true", help="total fn ran - fns ran 1 second before")
        parser.add_option('-C','--command', help="command to run for capture")
        parser.add_option('-i','--interval', help="prerun time before capture")
        parser.add_option('-r','--reverse',default=False, action="store_true",  help="reverse the Sort")
        parser.add_option('-t','--showtot',default=True, action="store_false",  help="show total fn")
        options, remainder = parser.parse_args()
        self.prerun, self.fn = {}, {}
        
        #defaults
        self.dur = 10
        if options.duration: self.dur = int(options.duration)
        self.sort = 'hit'
        if options.sort: self.sort = options.sort
        try:
            self.cpu = set(map(int,options.cpu)) if options.cpu else os.sched_getaffinity(0)
        except:
            self.cpu = set(range(multiprocessing.cpu_count()))
        self.excl,self.rev,self.cmd,self.tot = options.exclusive,options.reverse,options.command,options.showtot
        self.int = 1
        if options.interval: self.int = int(options.interval)
        if self.sort not in ('hit','tim','avg'):
            parser.error("Option sort : either hit, tim, avg")
            sys.exit(1)

    def sighand(self, sig, frame):
        self.disable()
        self.postprocess()
        sys.exit(0)

    def enable(self): # enable stat collection echo 1 > function_profile_enabled
        os.system("echo 1 > /sys/kernel/debug/tracing/function_profile_enabled")

    def disable(self):
        os.system("echo 0 > /sys/kernel/debug/tracing/function_profile_enabled")

    def preprocess(self):
        os.system("echo 0 > /sys/kernel/debug/tracing/options/sleep-time")
        self.prerun = {}
        if self.excl:
            self.enable()
            time.sleep(self.int)
            self.disable()
            self.iterate(self.process)
            self.prerun = self.fn
            self.fn = {}

    def postprocess(self):
        self.iterate(self.process)
        cnt=0
        for k,v in sorted(self.fn.items(), key=lambda i: i[1][self.sort], reverse=self.rev):
            if k in self.prerun: continue
            print("%40s \t %12d \t %12d \t %.1f" %(k,v['hit'],v['tim'],v['avg']))
            cnt+=1
        if self.tot: print("Total: ",cnt)

    def process(self, f, c):
        if int(c) not in self.cpu: return # skip non-interesting cpus
        fp = open(f,'r')
        try:
            l = fp.readline()
            while l:
                m = re.search(r'(\S+)\s+(\d+).*?(\d+).*?(\d+).*?(\d+)', l)
                if m and len(m.groups()) == 5:
                    k = m.group(1)
                    if k not in self.fn: self.fn[k] = {}
                    h = self.fn[k]
                    h.setdefault('cpu',set()).add(c)
                    n = len(h['cpu'])
                    h['hit'] = h.get('hit',0) + int(m.group(2)) # sum of hits
                    h['tim'] = h.get('tim',0) + int(m.group(3)) # sum of time
                    h['avg'] = float(h['tim']) / h['hit']
                l = fp.readline()
        finally:
            fp.close()

    def iterate(self, fn=None):
        dir = "/sys/kernel/debug/tracing/trace_stat/"
        if not os.listdir(dir):
            raise Exception("kernel debug tracing not mounted or feature not enabled")

        for f in os.listdir(dir):
            if f.startswith("function"):
                c = re.findall("\d+", f)[0]             
                if fn:
                    fn(dir+'/'+f,c)

    def run(self):
        self.preprocess()
        if not self.cmd: tmpstr = 'sleep ' + str(self.dur)
        else: tmpstr = self.cmd
        print("HIT CTRL-C to stop. Running '%s'" % tmpstr)
        self.enable()
        if self.cmd:
            os.system(self.cmd)
        else:
            time.sleep(self.dur)
        self.disable()

        self.postprocess()

if __name__ == '__main__':
    gfn = gfunccount()
    gfn.run()
