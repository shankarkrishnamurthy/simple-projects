static etcd cluster:
https://coreos.com/etcd/docs/latest/dev-guide/local_cluster.html
https://devopscube.com/setup-etcd-cluster-linux/
https://coreos.com/etcd/docs/latest/demo.html


etcd cluster (consensus/leader election) alternative:zookeeper
===============================================


dnf install etcd (3.2.16)
[root@abacus-fc29 ~]# export ETCDCTL_API=3
[root@abacus-fc29 ~]# etcdctl version
etcdctl version: 3.2.16
API version: 3.2

CLUSTER is UP. Execute basic operation
---------------------------------------

[root@abacus-fc29 ~]# etcdctl member list
a84d8036d3b43083, started, infra0, http://10.217.202.38:2380, http://10.217.202.38:2379
cd9194143ac230ac, started, infra2, http://10.221.50.14:2380, http://10.221.50.14:2379
f1d07547a8b9ccd4, started, infra1, http://10.217.202.140:2380, http://10.217.202.140:2379
[root@abacus-fc29 ~]# echo $ETCDEP
http://10.217.202.38:2380,http://10.221.50.14:2380,http://10.217.202.140:2380
[root@abacus-fc29 ~]# etcdctl --endpoints=$ETCDEP -w table endpoint status
[root@abacus-fc29 ~]# etcdctl set foo bar # set key
[root@abacus-fc29 ~]# etcdctl get --prefix '' # gets all keys with prefix
[root@abacus-fc29 ~]# etcdctl watch foo --hex
[root@galata-fc29 ~]# etcdctl del foo


REMOVING an Existing Etcd Member:
---------------------------------
[root@abacus-fc29 ~]# etcdctl member remove a84d8036d3b43083

ADDING an Member onto Existing cluster: On a Node which is currently member
---------------------------------------
[root@abacus-fc29 ~]# etcdctl member add infra4 --peer-urls=http://10.217.211.130:2380
Member adca39db3770202e added to cluster bf742ea517fdc9c2

ETCD_NAME="infra4"
ETCD_INITIAL_CLUSTER="infra4=http://10.217.211.130:2380,infra2=http://10.221.50.14:2380,infra1=http://10.217.202.140:2380"
ETCD_INITIAL_CLUSTER_STATE="existing"
[root@abacus-fc29 ~]# 
Member a84d8036d3b43083 removed from cluster bf742ea517fdc9c2
[root@abacus-fc29 ~]#

On the Node that is getting added
#!/bin/bash
etcd --name infra4 --initial-advertise-peer-urls http://10.217.211.130:2380 \
  --listen-peer-urls http://10.217.211.130:2380 \
  --listen-client-urls http://10.217.211.130:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.217.211.130:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra4=http://10.217.211.130:2380,infra1=http://10.217.202.140:2380,infra2=http://10.221.50.14:2380 \
  --initial-cluster-state existing


RESETTING cluster
------------------
rm -rf /var/lib/etcd*
reboot

USING RUNTIME INTERACTION with ETCD
------------------------------------
[root@zela-f29 ~]# curl -L http://127.0.0.1:2379/version
{"etcdserver":"3.2.16","etcdcluster":"3.2.0"}

PUT/GET/ ... all can be done with this URL

GET CLUSTER STATUS
-------------------
etcdctl --endpoints=$(etcdctl member list -w json | jq '.members[] | .clientURLs[0]' | xargs | sed -e 's/ /,/g') endpoint status -w table
+----------------------------+------------------+---------+---------+-----------+-----------+------------+
|          ENDPOINT          |        ID        | VERSION | DB SIZE | IS LEADER | RAFT TERM | RAFT INDEX |
+----------------------------+------------------+---------+---------+-----------+-----------+------------+
| http://10.217.202.140:2379 |  2ae090259d20843 |  3.2.16 |   25 kB |     false |        14 |         11 |
| http://10.217.211.130:2379 | d400be1019e5c539 |  3.2.16 |   25 kB |      true |        14 |         11 |
|   http://10.221.50.14:2379 | eb964de41e9aab5a |  3.2.16 |   25 kB |     false |        14 |         11 |
+----------------------------+------------------+---------+---------+-----------+-----------+------------+


=======================================================
