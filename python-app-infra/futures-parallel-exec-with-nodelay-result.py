import concurrent.futures as p
import math,os
import signal, psutil
 
PRIMES = [
    112582705942171,
    112272535095293,
    115280095190773,
    115797848077099,
    1099726899285419]
 
def is_prime(n):
    if n % 2 == 0:
        return (n,False)
 
    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return (n,False)
    return (n,True)

def main():
        e =p.ProcessPoolExecutor(max_workers=4)

        fl = [e.submit(is_prime,f) for f in PRIMES]
        while True:
            d,nd= p.wait(fl,timeout=3,return_when=p.FIRST_COMPLETED)
            if not len(d):
                print("Rest of Future timedout", nd)
                for i in nd:
                    try:
                        print(i.result(timeout=1) )
                    except Exception as e:
                        print(e) # TimeoutError
                current_process = psutil.Process()
                children = current_process.children(recursive=True)
                for child in children:
                    print('Child pid is {}'.format(child.pid))
                    child.send_signal(signal.SIGKILL)
                break
            for i in d:
                print("RESULT: ",i.result())
            if not len(nd):
                print("All tasks done");
                break
            fl = list(nd)

if __name__ == '__main__':
    main()
