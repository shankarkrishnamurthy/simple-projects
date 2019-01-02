#!/bin/env python
import sys, os
import subprocess
import json

def do_call(execfile):
    try:
        print "Running Command: ", execfile
        proc = subprocess.Popen(execfile, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        return out
    except:
        print " %s failed" % execfile

def gettags(repo):
    url='https://hub.docker.com/v2/repositories/%s/tags?page_size=1024&page=%d'
    pg = 1
    out = do_call(['curl','-L','s',url % (repo,pg) ])
    #print out
    jo = json.loads(out)
    if 'count' not in jo: 
        print "Cannot find repo"
        sys.exit(1)
    cnt,res = jo['count'], jo['results']
    rescnt = len(res)
    tags = map(lambda x: x['name'], res)
    while rescnt < cnt:
        pg+=1
        out = do_call(['curl','-L','s',url % (repo,pg) ])
        #print out
        jo = json.loads(out)
        res = jo['results']
        rescnt += len(res)
        tags += map(lambda x: x['name'], res)
        
    return tags

if __name__ == '__main__':
    print sys.argv
    if len(sys.argv) < 2:
        print "Enter repo name"
        sys.exit(1)

    repo = sys.argv[1]
    tl = gettags(repo)

    print '%s:' % repo
    for n in tl: print (n)
    print 'Total : %d' % len(tl)
