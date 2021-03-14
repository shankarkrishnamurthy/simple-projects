#!/usr/bin/env python
#
# Description: Pipelined Indexer for NetScaler Support Packages
# Date: Aug 2019 
# Author: Shankar, K
#

from threading import *
from pprint import pprint
from datetime import datetime
from daemon import Daemon
import os, sys, time
import tempfile
import subprocess
import re
import json
import tarfile
import optparse
import shutil
import pickle
import pipes
import logging

sys.path.append(os.path.abspath('./py-modules'))
import requests
import yaml

conf,debug = {},0
def PPRINT(a):
    if debug:pprint(a)

def exec_cmd(cmd):
    out, err = subprocess.Popen(cmd, shell=True,
                  stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
    return (out,err)


class Agent(object):
    def __init__(self):
        self.srQ = []
        self.srQevt = Event()
        self.dataQ = []
        self.dataQevt = Event()
        self.done = Event()
        self.pdone = 0
        self.pdoneLock = Lock()

    def get_all_id(self,p, np):

        def matpat(p,i):
            for pat in p:
                try: m = pat.search(i)
                except: pass
                if m: 
                    t = m.group(1)
                    if not t: t=m.group(0)
                    #logging.info(m.groups(),t)
                    t=t.replace('.tar.gz','')
                    t=t.replace('.tar.bz2','')
                    t=t.replace('.tgz','')
                    return t,pat.pattern
            return None,None

        fs={}
        for r,d,f in os.walk(np):
            for pat in p:
                if pat.search(r): continue # if patten in dir. skip
            
            for i in f:
                fi = r+'/'+i
                #logging.info("Opening %s", fi)
                if not os.path.isfile(fi): continue
                try:
                    if not tarfile.is_tarfile(fi): continue
                    a = tarfile.open(fi)
                    n = a.next()
                    n = n.name if n else ""
                    t,pat = matpat(p,n)
                    #logging.info('2. %s : %s',n, t)
                    if t: 
                        fs[t] = (fi,pat)
                        continue
    
                    if re.match('SDX',i):
                        for b in a.getnames():
                            t,pat = matpat(p,b)
                            #logging.info('3. ', b, t)
                            if t: 
                                fs[t] = (fi,pat,b)
                except:
                    logging.info("Failed to Parse %s", fi)
                    continue
                    
        return fs


    # pkg key=ID (uniq id for pkg within SR)
    # pkg[key][0]=tarball
    # pkg[key][1]=Pattern that led this match
    # pkg[key][2]=internal tarball if pkg[0] is SDX uber tarball
    def extract(self, sr, f, pkg):
        def deltemp(t): 
            try: 
                if t: shutil.rmtree(t)
            except: pass
        d = {'SR': sr}
        #logging.info(' extract %s', f)
        #logging.info(' pkg %s', pkg)
        d['PKG'] = set()
        d['FILES'] = {}
        for k in pkg.keys():
            d.setdefault('PKG', set()).add(k)
            tball,pat,t=pkg[k][0],pkg[k][1],None
            bname = os.path.basename(tball)
            if re.match('SDX', bname) and len(pkg[k]) > 2:
                fte = pkg[k][2]
                t = tempfile.mkdtemp()   
                cmd = "tar -C %s -xzf %s %s" % (t, re.escape(tball), fte)
                out,err = exec_cmd(cmd)
                if err: 
                    deltemp(t)
                    continue
                tball=t+'/'+fte

            flg = '-tjf' if tball[-3:]=='bz2' else '-tzf'
            cmd = "tar %s %s " % (flg,re.escape(tball))
            for p in f[pat]:
                cmd +=" --include=%s " % p
            #logging.info("FindFile: %s\n", cmd)
            out,err = exec_cmd(cmd)

            #logging.info("Output: %s %s",tball, out.splitlines())
            #logging.info("Err: %s",err.splitlines())
            flg = '-xjf' if tball[-3:]=='bz2' else '-xzf'
            for i in out.splitlines():
                cmd = "tar -O %s %s %s" % (flg, re.escape(tball),i)
                #logging.info("Extract: %s\n", cmd)
                out,err = exec_cmd(cmd)
                if err: 
                    deltemp(t)
                    continue
                #logging.info("Save content for %s ", i)
                mz =   100000 # ~ .1 MB
                if len(out) > mz*2:
                    d['FILES'][i] = out[:mz].decode("utf-8","ignore").encode("utf-8")
                    d['FILES'][i] += out[-mz:].decode("utf-8","ignore").encode("utf-8")
                else:
                    d['FILES'][i] = out[:mz].decode("utf-8","ignore").encode("utf-8")
            deltemp(t)

        return d

    def checkSR(self, sr, vport):
        url = 'http://'+vport+'/check'
        data = { 'SR': sr }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        try:
            r = requests.post(url, data=json.dumps(data), headers=headers)
        except Exception as e:
            raise(e)

        rsp = r.json()
        PPRINT(rsp)
        return r.status_code == 200 and not rsp['present']

    def saveSR(self,d,vport):
        url = 'http://'+vport+'/'+d['SR']
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        d['PKG'] = list(d['PKG'])
        try:
            r = requests.post(url, data=json.dumps(d), headers=headers)
        except Exception as e:
            raise(e)

        rsp = r.json()
        PPRINT(rsp)

    def saveLUT(self,vport):
        url = 'http://'+vport+'/lut'
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        try:
            r = requests.post(url, headers=headers)
        except Exception as e:
            raise(e)
        rsp = r.json()

    def signalSR(self, sr):
        self.srQ.append(sr)
        self.srQevt.set()

    def signalDQ(self, d):
        self.dataQ.append(d)
        self.dataQevt.set()

    def MonitorThread(self, path, vport):
        srcnt = 0
        # while True: trigger condition needed! ( *** LATER *** )
        if options.sr:
            if debug: logging.info('SR = %s', options.sr)
            if re.search('^\d{8}$', options.sr):
                if self.checkSR(options.sr, vport):
                    self.signalSR(options.sr)
                    srcnt += 1

        elif options.debugfile:
            if debug: logging.info('DBG FILE = %s', options.debugfile)
            f = open(options.debugfile, 'r')
            for sr in f:
                sr = sr.rstrip()
                if not re.search('^\d{8}$', sr): continue
                if self.checkSR(sr,vport): 
                    self.signalSR(sr)   
                    srcnt += 1
            f.close()

        else:
            
            if debug: logging.info('WALK DIR = %s', path)
            for sr in os.listdir(path):
                if not re.search('^\d{8}$', sr): continue
                if self.checkSR(sr,vport): 
                    self.signalSR(sr)   
                    srcnt += 1
            self.saveLUT(vport)

        logging.info("Total SR processed: %s", srcnt)
        self.done.set()
        self.srQevt.set()

    def ProcessThread(self,path,files):
        # deques jobs and starts working on it
        # populates rawdata once done

        p = map(re.compile,files.keys())
        while True:
            self.srQevt.wait()
            self.srQevt.clear()
            while self.srQ:
                sr = self.srQ.pop()
                np = path+'/'+ sr
                #logging.info('Processing ... %s', np)
                idlist = self.get_all_id(p, np)
                #logging.info("%s %s",np, idlist)
            
                # extract the content of each files
                data = self.extract(sr, files, idlist)
                self.signalDQ(data)

            if self.done.is_set(): break
        with self.pdoneLock:
            self.pdone += 1
        self.dataQevt.set()

    def SenderThread(self, vport, npthr,path):
        while True:
            self.dataQevt.wait()
            self.dataQevt.clear()
            while self.dataQ:
                d = self.dataQ.pop()
                #logging.info('SR %s', d['SR'])
                #logging.info('PKG %s',d['PKG'])
                #logging.info('Send Data %s',d.keys())
                #logging.info('')
                try:
                    d['LAT']=os.path.getatime(path+'/'+d['SR'])
                    d['LMT']=os.path.getmtime(path+'/'+d['SR'])
                except: continue
                self.saveSR(d,vport)
            
            if not self.srQ and self.pdone > npthr-1:  break
    
def die(obj, msg):
    logging.info(msg)
    if obj:
        obj.done.set()
        obj.srQevt.set()
        obj.dataQevt.set()
    sys.exit(1)

def main(obj):
    logging.basicConfig(filename='/tmp/agent.log',level=logging.INFO,format='%(asctime)s %(message)s')
    logging.info("Starting the process")
    if options.config: conf["file"] = options.config
    else: conf['file'] = os.path.dirname(obj.invokedir) + '/agent.conf'
    fl = yaml.load(open(conf['file']), Loader=yaml.FullLoader)
    for k in fl.keys():
        if k[0:2] == "x-": 
            fl.update(fl[k])
            del fl[k]
        if k[0:2] == "y-": 
            conf.update(fl[k])
            del fl[k]
    PPRINT(fl)
    PPRINT(conf)

    pt,npthr =[], 3
    agent = Agent()

    mt = Thread(target=agent.MonitorThread, args=([conf["path"],conf["agentPort"]]))

    for i in range(npthr):
        pt.append(Thread(target=agent.ProcessThread, args=([conf["path"],fl])))

    st = Thread(target=agent.SenderThread, args=([conf["agentPort"],npthr,conf["path"]]))

    d1 = datetime.now()

    mt.start()
    for i in range(npthr): pt[i].start()
    st.start()

    st.join()
    for i in range(npthr): pt[i].join()
    mt.join()

    d2 = datetime.now()
    logging.info('%d days %d hr %d min %d sec %d total secs',\
            (d2-d1).days,\
            (d2-d1).seconds/3600,((d2-d1).seconds%3600)/60, ((d2-d1).seconds%3600) % 60,\
            (d2-d1).total_seconds())

class AgentDaemon(Daemon):
    def __init__(self,pf):
        Daemon.__init__(self, pf)
    def run(self):
        main(self)

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option('-c','--config', default=False,  help="config file for indexing" )
    parser.add_option('-d','--debugfile', default=False,  help="file containing SR number" )
    parser.add_option('--start', default=False, action="store_true",  help="SR " )
    parser.add_option('--stop', default=False, action="store_true", help="SR " )
    parser.add_option('--sr', default=False,  help="SR number to process" )
    parser.add_option('--version', default=1.0, type="float", )
    options, remainder = parser.parse_args()

    d = AgentDaemon('/tmp/agent.pid')

    if options.start: 
        d.start()
    elif options.stop: 
        d.stop()
    else:
        d.invokedir = os.path.abspath(__file__)
        main(d)

