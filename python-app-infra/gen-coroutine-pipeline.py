#!/bin/env python3
#
# Simple pipeline using coroutines/generators
#
#           / stage 2a \
#   stage1              stage 3
#           \ stage 2b /
#
import inspect
def stage1(i):
    rc = -1
    while True:
        v1 = (yield rc)
        print ("In Func " + inspect.stack()[0][3])
        if (int(v1) % 2 == 0): n = i + 1
        else: n = i + 2
        rc = gl[n].send(n)

def stage2a(i):
    rc = -1
    while True:
        v1 = (yield rc)
        print ("In Func " + inspect.stack()[0][3])
        rc = gl[-1].send(len(gl)-1)

def stage2b(i):
    rc = -1
    while True:
        v1 = (yield rc)
        print ("In Func " + inspect.stack()[0][3])
        rc = gl[-1].send(len(gl)-1)

def stage3(i):
    rc = -1
    while True:
        v1 = yield rc
        print ("In Func " + inspect.stack()[0][3])
        rc = v1 + 1

fl = [stage1, stage2a, stage2b, stage3]
gl = ([i(0) for i in fl])
[next(i) for i in gl] # [-1,-1,-1,-1]
print (gl[0].send(1))
#print (gl[0].send(2))
