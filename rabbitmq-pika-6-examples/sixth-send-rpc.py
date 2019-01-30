#!/usr/bin/env python
import pika as p
import uuid

class FibonacciRpcClient(object):
    def __init__(self):
        self.conn=p.BlockingConnection(p.ConnectionParameters(host='localhost'))
        self.channel = self.conn.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.cq = result.method.queue # callback_queue
        self.channel.basic_consume(self.on_response, no_ack=True, queue=self.cq)

    def on_response(self, ch, method, props, body):
        if self.ci == props.correlation_id: self.response = body

    def call(self, n):
        self.response = None
        self.ci = str(uuid.uuid4()) # correlation id
        pr=p.BasicProperties(reply_to=self.cq,correlation_id=self.ci,)
        self.channel.basic_publish(exchange='', routing_key='rpc_queue',
            properties=pr, body=str(n))
        while self.response is None: self.conn.process_data_events()
        return int(self.response)

fibonacci_rpc = FibonacciRpcClient()
print(" [x] Requesting fib(30)")
response = fibonacci_rpc.call(30)
print(" [.] Got %r" % response)
