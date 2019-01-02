#!/usr/bin/env python3

import redis

redis_host = "localhost"
redis_port = 6379
redis_password = ""

def hello_redis():
    """Example Hello Redis Program"""
    
    try:
        # The decode_repsonses flag here directs the client to convert the responses from Redis into Python strings
        # using the default encoding utf-8.  This is client specific.
        r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
    
        print ('Current keys ', r.keys())
        for k in r.keys():
            print (r.type(k))
            #print (k,' : ', r.get(k))

        r.set("msg:hello", "Hello Redis!!!")
        msg = r.get("msg:hello")
        print(msg)        

        udict = { "Name": "Shankar", "Age" : 50 }
        r.hmset("pyDict", udict)
        print (r.hgetall("pyDict"))

        #r.lpush("pyList", "what")
        #r.lpush("pyList", "ever")
        print (r.lrange("pyList",0,r.llen("pyList")))

        r.delete("msg:hello")
        r.delete("foo:01")
        r.delete("key:00")

    
    except Exception as e:
        print(e)

if __name__ == '__main__':
    hello_redis()
