from concurrent.futures import ThreadPoolExecutor
from time import sleep
 
def return_after_5_secs(message):
    sleep(5)
    return message+' returned'
 
pool = ThreadPoolExecutor(3) # default 5
 
future = pool.submit(return_after_5_secs, ("hello"))
print(future.done())
while not future.done():
    sleep(1)
print(future.done())
print(future.result())
