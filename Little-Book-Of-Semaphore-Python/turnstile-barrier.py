from threading import *
import time
class Barrier :
    def __init__(self , n):
        self .n = n
        self.count = 0
        self.mutex = Semaphore(1)
        self.turnstile = Semaphore(0)
        self.turnstile2 = Semaphore(0)
    
    def phase1( self ):
        self.mutex.acquire()
        self.count += 1
        if self.count == self.n:
            print("All have reached Rendevous point A")
            for j in range(self.n): self.turnstile.release()
        self.mutex.release()
        self.turnstile.acquire() # release ALL at same time

    def phase2( self ):
        self.mutex.acquire()
        self.count -= 1
        if self.count == 0:
            print("All have reached Rendevous point b")
            self.turnstile2.release()
        self.mutex.release()
        self.turnstile2.acquire()
        self.turnstile2.release() # Release one-by-one

    def acquire( self ):
        self.phase1()
        self.phase2()

def run(b,i):
    b.phase1()
    # n thread can potentially cross this at same time
    b.phase2()
    # 1 thread can potentially cross this at any time

if __name__ == '__main__':
    N = 5
    b = Barrier(N)
    for i in range(N):
        Thread(target=run, args=(b,i,)).start()
    time.sleep(10)
