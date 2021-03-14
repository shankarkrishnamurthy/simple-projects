#!/bin/env python3
import datetime
import redis

import opentracing
import redis_opentracing

# Your OpenTracing-compatible tracer here.
tracer = opentracing.Tracer()

if __name__ == '__main__':
    client = redis.StrictRedis()

    # By default, init_tracing() traces all Redis commands.
    redis_opentracing.init_tracing(tracer)

    with tracer.start_active_span('main_span'):

        # Traced as a SET command,
        # with main_span as implicit parent.
        print (datetime.datetime.now())
        client.set('last_access', str(datetime.datetime.now()))

        # Traced as a MULTI command with
        # SET key:00 what
        # SET foo:01 bar
        pipe = client.pipeline()
        pipe.set('key:00', 'what')
        pipe.set('foo:01', 'bar')
        print(pipe.execute())
