#!/bin/env python3

import redis
import time
import traceback

def RedisCheck():
    try:
        r = redis.StrictRedis(host='localhost', port=6379)

        p = r.pubsub() 
        p.subscribe('startScripts')
        PAUSE = True

        while PAUSE:
            print("Waiting For redisStarter...")
            message = p.get_message() 
            if message:
                command = message['data']  

                if command == b'START':
                    PAUSE = False  

            time.sleep(1)

        print("Permission to start...")

    except Exception as e:
        print("!!!!!!!!!! EXCEPTION !!!!!!!!!")
        print(str(e))
        print(traceback.format_exc())

if __name__ == "__main__":
    RedisCheck()
