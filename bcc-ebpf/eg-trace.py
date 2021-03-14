#!/bin/env python
# Descripton:
#   Program to use trace points and trace buffer to transfer info. Uses Array.
# Author: K.Shankar
# Date: May 2020
#
from bcc import BPF
from ctypes import *

prog="""
BPF_ARRAY(reason,u32,5);
TRACEPOINT_PROBE(tlb,tlb_flush)
{
    int r = args->reason;
    u32 *v = reason.lookup(&r);
    if (v) (*v)++;
    bpf_trace_printk("%d %d\\n",args->reason, args->pages);
    return 0;
}

"""

rstr = ["flush on task switch" , "remote shootdown" , "local shootdown" , "local mm shootdown" , "remote ipi send" ]
b = BPF(text=prog)
while True:
    try:
        (task, pid, cpu, flags, ts, msg) = b.trace_fields()
        r,p = msg.split(b" ")
        if int(r)!=0: # just to reduce too-much printing
            print(task, pid, cpu, flags, ts, msg)
    except ValueError:
        continue
    except KeyboardInterrupt:
        e = b["reason"]
        print()
        for i in range(5):
            print(i,' ',rstr[i],' ',e[i].value)
        exit()
