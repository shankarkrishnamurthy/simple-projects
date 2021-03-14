#!/bin/bash

# RUNNING ETCD is pre-requisite
etcdctl set  /atomic.io/network/config '{"Network": "18.16.0.0/16", "SubnetLen": 24, "Backend": { "Type": "vxlan", "VNI": 1 }}'

service flanneld restart

service docker restart

ifconfig docker0
ifconfig flannel.1
ip route

docker run --rm -it alpine:latest /bin/sh

 # ping 18.16.92.3 -c 3

