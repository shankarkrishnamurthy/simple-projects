#!/bin/env python3
#
# Author: Shankar, K
# Date: Dec 2018
#
# Description: Simple Microservice which monitors the Health of SDX
# and publishes the health over the 'RabbitMQ' message broker
#
from nameko.rpc import rpc

class SDXHealth(object):
    name = "SDXHealth"
    _redis = None
    _shared = None
    _dispatch = None

    @rpc
    def Run(self,payload):
        print ("Called " + payload)
        return 0
        #a = mp.Process(target=self.ConsoleHealth, args=(self.sdx,))
        #a.start()

