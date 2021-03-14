from heapq import *
from db import *
from notif import *

class driver():
    def __init__(self,d):
        self.q = []
        self.d = d
        self.n = notif()

    def _process(self):
        for r in self.d.getall():
            if r[Schema.DONE_COL] == False:
                heappush(self.q,(r[Schema.NOTIF_COL].strftime("%Y%m%d"),r))
        print("_process ",self.q)

    def calculate_timeout(self):
        if not self.q:
            return None 
        r = self.q[0][1]
        d1 = r[Schema.NOTIF_COL] - date.today()
        diff = d1.total_seconds()
        return (diff if diff >0 else 0)

    def handle_message(self):
        self.d.conn.poll()
        while self.d.conn.notifies:
          n = self.d.conn.notifies.pop()
          print(' pid ', n.pid, ' ch name ', n.channel, ' row ', n.payload)
          r = eval(n.payload.replace('true','True').replace('false','False'))
          if n.channel == 'create_chan':
            print("Add Entry ",r)
            key = r[Schema.NOTIF_HDR].replace('-','')
            r[Schema.NOTIF_HDR] = datetime.strptime(r[Schema.NOTIF_HDR],'%Y-%m-%d').date()
            r[Schema.FDATE_HDR] = datetime.strptime(r[Schema.FDATE_HDR],'%Y-%m-%d').date()
            heappush(self.q, (key,tuple(r.values())))
          elif n.channel == 'delete_chan':
            print("Remove entry",r);
            for i in self.q:
              if r["snum"] == i[1][0]:
                self.q.remove(i)
                heapify(self.q)
                # Update row in DB active flag = 0
                break
          else: pass

    def handle_timeout(self):
        print("handle timeout ", self.q[0][1])
        self.n.sms(self.q[0][1][1]) # Msg
        self.n.email()
        self.d.done(self.q[0][1][0]) # snum
        heappop(self.q)

    def eventloop(self):
        print("Starting eventloop thread")
        self._process()
        while True:
          t = self.calculate_timeout()
          # t = None if t==None else t/3600/24 # debug line for testing
          print("Timeout = ", t, " q len ", len(self.q))
          r,w,x = select.select([self.d.conn],[],[],t)
          if r:
            self.handle_message()
          else:
            self.handle_timeout()

if __name__ == '__main__':
    db = DB()
    d = driver(db)
    d.eventloop()
    d.close()
