#!/bin/env python

import asyncio
import time

async def mycoroutine(o,ttp):
    print(f"getting {o} order")
    await asyncio.sleep(ttp)
    #time.sleep(ttp)
    print(o, "ready")
    return ttp+100

async def driver():
    await loop.create_task(mycoroutine("pasta", 7))
    await loop.create_task(mycoroutine("salad", 10))
    await loop.create_task(mycoroutine("burger", 3))

    c1 = loop.create_task(mycoroutine("pasta", 7))
    c2 = loop.create_task(mycoroutine("salad", 10))
    c3 = loop.create_task(mycoroutine("burger", 3))
    tasks = [c1,c2,c3]
    await asyncio.wait(tasks)

    ct = [mycoroutine("pasta", 7), 
            mycoroutine("salad", 10), 
            mycoroutine("burger", 3)]
    await asyncio.gather(*ct)

    return (c1,c2,c3)

loop = asyncio.get_event_loop()
c1,c2,c3 = loop.run_until_complete(driver())
print(c1.result(),c2.result(),c3.result())
loop.close()

