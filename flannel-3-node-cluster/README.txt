=======================================================

flannel 3 node cluster
----------------------

some references used:
---------------------
flannel-and-etcd-with-docker.sh:
http://www.colliernotes.com/2015/01/flannel-and-docker-on-fedora-getting.html
https://gist.github.com/dbathgate/737e8d800decde9adbf8a0130870bcc4#file-flannel-and-etcd-with-docker-sh
https://blog.laputa.io/kubernetes-flannel-networking-6a1cb1f8ec7c
https://msazure.club/flannel-networking-demystify/

start etcd https://github.com/shankarkrishnamurthy/simple-projects/tree/master/etcd-3-node-cluster
---------------------------------------------------------------

First:
------
[root@zela-f29 etcd-3-node-cluster]# etcdctl member list
64e919397c41c33: name=infra2 peerURLs=http://10.221.50.14:2380 clientURLs=http://10.221.50.14:2379 isLeader=false
319536976cd45999: name=infra3 peerURLs=http://10.217.202.140:2380 clientURLs=http://10.217.202.140:2379 isLeader=false
d400be1019e5c539: name=infra1 peerURLs=http://10.217.211.130:2380 clientURLs=http://10.217.211.130:2379 isLeader=true

Second:
-------
Apply flannel config to etcd
For flannel, we need to have key - value config
[root@zela-f29 etcd-3-node-cluster]# cat ~/flannel-config.json 
{
    "Network": "18.16.0.0/16",
    "SubnetLen": 24,
    "Backend": {
        "Type": "vxlan",
        "VNI": 1
     }
}

[root@zela-f29 ~]# etcdctl -version
etcdctl version: 3.2.16
API version: 2
(one time: put this config into etcd)
[root@zela-f29 ~]# etcdctl set /atomic.io/network/config < flannel-config.json
(or)
curl -L http://localhost:2379/v2/keys/coreos.com/network/config -XPUT --data-urlencode value@flannel-config.json

Third:
-------
Start Flanneld service:
[root@zela-f29 etcd-3-node-cluster]# cat /etc/sysconfig/flanneld | grep -ve '^$\|^#'
FLANNEL_ETCD_ENDPOINTS="http://127.0.0.1:2379"
FLANNEL_ETCD_PREFIX="/atomic.io/network"
[root@zela-f29 ~]# service flanneld start
[root@zela-f29 ~]# 
[root@zela-f29 ~]# cat /lib/systemd/system/flanneld.service 
...
[Service]
ExecStart=/usr/bin/flanneld -etcd-endpoints=${FLANNEL_ETCD_ENDPOINTS} -etcd-prefix=${FLANNEL_ETCD_PREFIX} $FLANNEL_OPTIONS
ExecStartPost=/usr/libexec/flannel/mk-docker-opts.sh -k DOCKER_NETWORK_OPTIONS -d /run/flannel/docker

[root@zela-f29 ~]# cat /run/flannel/subnet.env 
FLANNEL_NETWORK=18.16.0.0/16
FLANNEL_SUBNET=18.16.17.1/24
FLANNEL_MTU=1450
FLANNEL_IPMASQ=false
[root@zela-f29 ~]# cat /run/flannel/docker 
DOCKER_OPT_BIP="--bip=18.16.17.1/24"
DOCKER_OPT_IPMASQ="--ip-masq=true"
DOCKER_OPT_MTU="--mtu=1450"
DOCKER_NETWORK_OPTIONS=" --bip=18.16.17.1/24 --ip-masq=true --mtu=1450"

ps auxw | grep flanneld
root     23053  0.0  0.0 3978472 26964 ?       Ssl  10:33   0:00 /usr/bin/flanneld -etcd-endpoints=http://127.0.0.1:2379 -etcd-prefix=/atomic.io/network

flannel subnets
---------------
[root@zela-f29 ~]# etcdctl ls /atomic.io/network/subnets/
/atomic.io/network/subnets/18.16.17.0-24
/atomic.io/network/subnets/18.16.93.0-24
/atomic.io/network/subnets/18.16.92.0-24
[root@zela-f29 ~]# etcdctl get /atomic.io/network/subnets/18.16.17.0-24
{"PublicIP":"10.217.211.130","BackendType":"vxlan","BackendData":{"VtepMAC":"56:d2:bc:13:bf:15"}}
[root@zela-f29 ~]# etcdctl get /atomic.io/network/subnets/18.16.93.0-24
{"PublicIP":"10.221.50.14","BackendType":"vxlan","BackendData":{"VtepMAC":"6a:4e:62:5d:02:e3"}}
(or)
[root@zela-f29 ~]# curl -Lq http://localhost:2379/v2/keys/atomic.io/network/subnets | json_pp


Fourth:
-------

restart docker service. It uses the above /run/flannel/docker directly to use the above network
from systemd drop-in facility (flannel.conf below)

   Loaded: loaded (/usr/lib/systemd/system/docker.service; enabled; vendor preset: disabled)
  Drop-In: /usr/lib/systemd/system/docker.service.d
           └─flannel.conf
   Active: active (running) since Mon 2019-01-21 10:34:49 PST; 32min ago

Checking flannel and docker:
----------------------------
[root@zela-f29 ~]# ip a s flannel.1 | grep inet
    inet 18.16.17.0/32 scope global flannel.1
    inet6 fe80::54d2:bcff:fe13:bf15/64 scope link 
[root@zela-f29 ~]# ip a s docker0 | grep inet
    inet 18.16.17.1/24 scope global docker0
    inet6 fe80::42:c1ff:fed9:2d9c/64 scope link 
[root@zela-f29 ~]# ip r 
default via 10.217.211.129 dev eno1 proto static metric 100 
10.217.211.128/25 dev eno1 proto kernel scope link src 10.217.211.130 metric 100 
18.16.17.0/24 dev docker0 proto kernel scope link src 18.16.17.1 
18.16.92.0/24 via 18.16.92.0 dev flannel.1 onlink 
18.16.93.0/24 via 18.16.93.0 dev flannel.1 onlink 

In another node:
----------------
[root@abacus-fc29 ~]# ip a s flannel.1 | grep inet
    inet 18.16.93.0/32 scope global flannel.1
    inet6 fe80::684e:62ff:fe5d:2e3/64 scope link 
[root@abacus-fc29 ~]# ip a s docker0 | grep inet
    inet 18.16.93.1/24 scope global docker0
    inet6 fe80::42:3bff:fe73:9319/64 scope link 
[root@abacus-fc29 ~]# ip r
default via 10.221.50.1 dev eno1 proto static metric 100 
10.221.50.0/24 dev eno1 proto kernel scope link src 10.221.50.14 metric 100 
18.16.17.0/24 via 18.16.17.0 dev flannel.1 onlink 
18.16.92.0/24 via 18.16.92.0 dev flannel.1 onlink 
18.16.93.0/24 dev docker0 proto kernel scope link src 18.16.93.1 linkdown 

ping two containers in two different nodes
------------------------------------------

Container 1:
------------
8544a6210b2e:~# ip a s | grep inet
    inet 127.0.0.1/8 scope host lo
    inet6 ::1/128 scope host 
    inet 18.16.17.2/24 scope global eth0
    inet6 fe80::42:12ff:fe10:1102/64 scope link 

container 2:
------------
9efc6510956c:~# ip a s | grep inet
    inet 127.0.0.1/8 scope host lo
    inet6 ::1/128 scope host 
    inet 18.16.92.2/24 scope global eth0
    inet6 fe80::42:12ff:fe10:5c02/64 scope link 

9efc6510956c:~# ping 18.16.17.2 -c 3
PING 18.16.17.2 (18.16.17.2): 56 data bytes
64 bytes from 18.16.17.2: seq=0 ttl=62 time=0.482 ms
64 bytes from 18.16.17.2: seq=1 ttl=62 time=0.395 ms
64 bytes from 18.16.17.2: seq=2 ttl=62 time=0.383 ms

--- 18.16.17.2 ping statistics ---
3 packets transmitted, 3 packets received, 0% packet loss
round-trip min/avg/max = 0.383/0.420/0.482 ms
9efc6510956c:~# 
[root@zela-f29 ~]# tcpdump -i flannel.1 icmp
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on flannel.1, link-type EN10MB (Ethernet), capture size 262144 bytes
11:41:57.830242 IP 18.16.92.2 > 18.16.17.2: ICMP echo request, id 8448, seq 0, length 64
11:41:57.830326 IP 18.16.17.2 > 18.16.92.2: ICMP echo reply, id 8448, seq 0, length 64
11:41:58.830341 IP 18.16.92.2 > 18.16.17.2: ICMP echo request, id 8448, seq 1, length 64
11:41:58.830399 IP 18.16.17.2 > 18.16.92.2: ICMP echo reply, id 8448, seq 1, length 64
11:41:59.830508 IP 18.16.92.2 > 18.16.17.2: ICMP echo request, id 8448, seq 2, length 64
11:41:59.830568 IP 18.16.17.2 > 18.16.92.2: ICMP echo reply, id 8448, seq 2, length 64

enable IP Forwarding 
---------------------
[root@zela-f29 ~]# sysctl -a | grep net.ipv4 | grep \\.forwarding
...
net.ipv4.conf.all.forwarding = 1
net.ipv4.conf.default.forwarding = 1
net.ipv4.conf.docker0.forwarding = 1
net.ipv4.conf.eno1.forwarding = 1
net.ipv4.conf.enp4s0f3.forwarding = 1
net.ipv4.conf.flannel/1.forwarding = 1
...

[root@zela-f29 ~]# iptables-save 
# Generated by iptables-save v1.8.0 on Mon Jan 21 11:46:12 2019
*nat
:PREROUTING ACCEPT [15:1430]
:INPUT ACCEPT [4:536]
:OUTPUT ACCEPT [862:52712]
:POSTROUTING ACCEPT [870:53354]
:DOCKER - [0:0]
-A PREROUTING -m addrtype --dst-type LOCAL -j DOCKER
-A OUTPUT ! -d 127.0.0.0/8 -m addrtype --dst-type LOCAL -j DOCKER
COMMIT
...
...
*filter
:INPUT ACCEPT [257174:21663210]
:FORWARD ACCEPT [6:504]
:OUTPUT ACCEPT [258029:21792661]
:DOCKER - [0:0]
:DOCKER-ISOLATION - [0:0]
-A INPUT -j KUBE-FIREWALL
-A FORWARD -j DOCKER-ISOLATION
-A FORWARD -o docker0 -j DOCKER
-A FORWARD -o docker0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
-A FORWARD -i docker0 ! -o docker0 -j ACCEPT
-A FORWARD -i docker0 -o docker0 -j ACCEPT
-A DOCKER-ISOLATION -j RETURN
COMMIT
# Completed on Mon Jan 21 11:46:12 2019

*IMPORTANT* Enable FORWARDING In flannel.1 is receiving but docker0 is not receiving
------------------------------------------------------------------------------------
[root@abacus-fc29 ~]# sudo iptables -P FORWARD ACCEPT

===============================================================

