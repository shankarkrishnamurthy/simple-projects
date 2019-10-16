import base64
import md5
from bisect import *
import numpy as np
class ConsistentHashing():
    def __init__(self,sl,nr): # server list, no. of replicas
        self.sl = sl
        self._hring = []
        self._hm = {}
        self.nr = nr
        for i in sl:
            h = str(i)
            rc = self.nr
            while rc > 0:
                h = self.hashfn(h)
                self._hring.append(h)
                self._hm[h] = str(i)
                rc -= 1
        self._hring.sort()
    
    def addMachine(self,id):
        self.sl.append(id)
        h = self.hashfn(str(id))
        rc = self.nr
        print 'Added m/c before ', len(self._hring),
        while rc > 0:
            h = self.hashfn(h)
            insort(self._hring,h)
            self._hm[h] = str(id)
            rc -= 1
        print ' after %d', len(self._hring)

    def delMachine(self,id):
        self.sl.remove(id)
        print 'deleted m/c before ', len(self._hring),
        for h,v in self._hm.items():
            if v == str(id):
                del self._hm[h]
                del self._hring[bisect_left(self._hring, h)]
        print ' after %d', len(self._hring)

    def getMachine(self,key):
        h = self.hashfn(key)
        i = bisect(self._hring, h)
        if i >= len(self._hring): i = 0
        m = self._hm[self._hring[i]]
        #print 'key %s hash %s picking machine %s machine_hash %s index %s' % (key,h,m,self._hring[i],i)
        return m
    def hashfn(self,k):
        m=md5.new(str(k))
        return base64.b64encode(m.digest())[:6] # limiting to 6 for readability only

def test1():
    global cs
    cs = ConsistentHashing([1,2],1000)
    #print cs._hring, cs._hm
    res = {}
    MIN,MAX=10000,20000
    for j in range(MIN,MAX):
        m = cs.getMachine(str(j))
        res[m] = res.get(m,0) + 1
    print res, 'std dev ', np.std(res.values())/(MAX-MIN)*100.0, ' % '

def test2():
    global cs
    for s in range(6,10):
        res = {}
        cs.addMachine(s)
        MIN=s*10000
        MAX=MIN+10000
        for j in range(MIN,MAX):
            m = cs.getMachine(str(j))
            res[m] = res.get(m,0) + 1
        print 'Added ', s, res, 'std dev ', np.std(res.values())/(MAX-MIN)*100.0,'%'
    
def test3():
    global cs
    for s in range(6,8):
        res = {}
        cs.delMachine(s)
        MIN=s*10000
        MAX=MIN+10000
        for j in range(MIN,MAX):
            m = cs.getMachine(str(j))
            res[m] = res.get(m,0) + 1
        print 'Deleted ', s, res, 'std dev ', np.std(res.values())/(MAX-MIN)*100.0,'%'

def test4():
    global cs
    cs = ConsistentHashing(['A','B','C','D','E'],250)
    res, kh = {} , []
    global MIN,MAX
    MIN,MAX=0,200000
    for j in range(MIN,MAX):
        m = cs.getMachine(str(j))
        res[m] = res.get(m,0) + 1
        kh.append((m,cs.hashfn(j))) 
    print res, 'std dev ', np.std(res.values())/(MAX-MIN)*100.0, ' % '
    cs.addMachine('F')
    res, kha = {} , []
    for j in range(MIN,MAX):
        m = cs.getMachine(str(j))
        res[m] = res.get(m,0) + 1
        kha.append((m,cs.hashfn(j))) 
    print res, 'std dev ', np.std(res.values())/(MAX-MIN)*100.0, ' % '
    s,d,c =0 , 0,0
    for i,j in zip(kh,kha):
        c+=1
        if i[0] == j[0]: s+=1
        else: d += 1
    print "Same ",s, " Diff ",d, ' Var ', 100.0*d/MAX,'%',100.0/len(cs.sl)
    global kh
    kh = kha

def test5():
    global cs
    cs.addMachine('G')
    res, kha = {} , []
    global MIN,MAX
    for j in range(MIN,MAX):
        m = cs.getMachine(str(j))
        res[m] = res.get(m,0) + 1
        kha.append((m,cs.hashfn(j))) 
    print res, 'std dev ', np.std(res.values())/(MAX-MIN)*100.0, ' % '
    s,d,c =0 , 0,0
    global kh
    for i,j in zip(kh,kha):
        c+=1
        if i[0] == j[0]: s+=1
        else: d += 1
    print "Same ",s, " Diff ",d, ' Var ', 100.0*d/MAX,'%',100.0/len(cs.sl)
    global kh
    kh = kha

def test6():
    global cs
    cs.addMachine('H')
    res, kha = {} , []
    global MIN,MAX
    for j in range(MIN,MAX):
        m = cs.getMachine(str(j))
        res[m] = res.get(m,0) + 1
        kha.append((m,cs.hashfn(j))) 
    print res, 'std dev ', np.std(res.values())/(MAX-MIN)*100.0, ' % '
    s,d,c =0 , 0,0
    global kh
    for i,j in zip(kh,kha):
        c+=1
        if i[0] == j[0]: s+=1
        else: d += 1
    print "Same ",s, " Diff ",d, ' Var ', 100.0*d/MAX,'%',100.0/len(cs.sl)
    global kh
    kh = kha

if __name__ == '__main__':

    # testing different keys with same set of servers
    print "\nTest 1\n"
    test1()

    print "\nTest 2\n"
    test2()

    print "\nTest 3\n"
    test3()

    # testing same set of keys but changing servers
    print "\nTest 4\n"
    test4()

    print "\nTest 5\n"
    test5()

    print "\nTest 6\n"
    test6()
