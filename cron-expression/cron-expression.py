#
#   *   *   *   *   *   ?   *
#  Sec Min Hrs Day Mon day  Year
# 
#   Day = date within a month (numerical) eg. 15-20
#   day = day of week (3 letter string) eg. MON,SUN
#
#   Description:
#       This script returns the next trigger time given an cron expression
#       To preserve the clarity, only 1st three variable of the expression is considered
#       But should have any problem extending to others (with minor modification) 
#
#       valid char: '/', '-', num, '*'
#           a/b: a is starting and freq is b
#
#   For simplicity - 
#       will not check error condition/values and assumes all inputs contains valid values
#
import time
import bisect as bi
class Solution(object):
    def __init__(self, p):
        #[s,m,h,D,m,d,y] = p.split(' ')
        w = p.split(' ')
        s,m,h = w[0],w[1],w[2]
        self.allow = []
        print w
        for e,a in zip([s,m,h],[60,60,24]):
            st_fr = e.split('/')
            st_en = e.split('-')
            allow_e = []
            #print 'E ',e,st_fr,st_en
            if len(st_fr)>1:
                st_fr[0] = 0 if st_fr[0] == '*' else st_fr[0]
                for i in range(int(st_fr[0]),a,int(st_fr[1])): 
                    allow_e.append(i)
            elif len(st_en) > 1:
                for i in range(int(st_en[0]),int(st_en[1])+1): allow_e.append(i)
            else: 
                if e == '*': 
                    for i in range(a): allow_e.append(i)
                else: allow_e.append(int(e))
            self.allow.append(allow_e)
        #print self.allow
        self.p = p
        self.allow = self.allow[::-1]

    # returns next trigger
    def eval(self):
        now = time.strftime("%H %M %S") #("%Y,%m,%d,%H,%M,%S")
        tl = map(int,now.split())
        next_avail = []
        assert(len(tl) == len(self.allow))
        for e,ct in zip(self.allow,tl):
            idx = bi.bisect_left(e,ct)
            next_avail.append(idx)
            i = len(next_avail)-1
            cl = self.allow[i]
            while i >= 0 and next_avail[i] == len(cl):
                next_avail[i] = 0 # this is just index
                i -= 1
                cl = self.allow[i]
                if i >= 0: 
                    cv = cl[next_avail[i]]
                    if cv == tl[i]: next_avail[i] += 1
            
        for i,e in enumerate(self.allow):
            next_avail[i] = str(e[next_avail[i]])
        return (now,'-'.join(next_avail))
            

print Solution('0 */3 * ? * * *').eval()
print Solution("10-30 * * ? * * *").eval()
print Solution("* * 2/4 ? * * *").eval()
print Solution("10-15 1/4 2/2 ? * * *").eval()
