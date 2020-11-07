#!/bin/env python
import os,sys
import multiprocessing
import time
import optparse
import re
import signal

class stacktrace:
    def __init__(self):
        os.system("mount -t debugfs none /sys/kernel/debug/ 2>/dev/null")
        signal.signal(signal.SIGINT, self.sighand)
        parser = optparse.OptionParser()
        options, remainder = parser.parse_args()
        parser.add_option('-c','--counthashstack',default=False, action="store_true",  help="hashes the stack and counts it. prints only the unique stacks (with count) at the end")
        if not remainder:
            parser.error("Provide atleast one fn() to back trace")
            exit(1)
        
        self.fn = remainder
        
    def sighand(self, sig, frame):
        self.disable()
        #self.postprocess()
        sys.exit(0)

    def call(self,cmd):
        rc = os.system(cmd)
        print('rc ', rc, ' cmd: ',cmd)
        return rc

    def enable(o): # enable stat collection echo 1 > function_profile_enabled
        rc = 0
        o.call("echo 0 > /sys/kernel/debug/tracing/tracing_on")
        o.call("echo > /sys/kernel/debug/tracing/set_ftrace_filter 2>/dev/null")
        for i in o.fn:
            rc += (o.call("echo %s >> /sys/kernel/debug/tracing/set_ftrace_filter 2>/dev/null"%i) != 0)
        if rc == len(o.fn):
            print("No fn() in symbol table. check /proc/kallsyms\n")
            exit(1);
        o.call("echo 1 > /sys/kernel/debug/tracing/options/func_stack_trace")
        o.call("echo function > /sys/kernel/debug/tracing/current_tracer")
        o.call("echo 1 > /sys/kernel/debug/tracing/tracing_on")
        o.f = open("/sys/kernel/debug/tracing/trace_pipe","r")

    def disable(o):
        o.call("echo 0 > /sys/kernel/debug/tracing/tracing_on")
        o.call("echo 0 > /sys/kernel/debug/tracing/options/func_stack_trace")
        # in order to work around file close problem. echo an noop func()
        o.call("echo kernel_init > /sys/kernel/debug/tracing/set_ftrace_filter")
        #o.call("echo nop > /sys/kernel/debug/tracing/current_tracer") will fail

    def run(self):
        self.enable()
        while 1:
            line = self.f.readline().rstrip()
            if line: print(line)

if __name__ == '__main__':
    bt = stacktrace()
    bt.run()

