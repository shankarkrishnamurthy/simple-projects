#!/bin/env python3
import redis

def WorkCheck():
    try:

        r = redis.StrictRedis(host='localhost', port=6379) 

        p = r.pubsub()

        print("Starting main scripts...")

        r.publish('startScripts', 'START')

        print("Done")

    except Exception as e:
        print("!!!!!!!!!! EXCEPTION !!!!!!!!!")
        print(str(e))
        print(traceback.format_exc())

if __name__ == "__main__":
    WorkCheck()
