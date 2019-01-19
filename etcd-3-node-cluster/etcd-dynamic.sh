NODE 1
------
etcd --name infra1 --initial-advertise-peer-urls http://10.217.211.130:2380 \
  --listen-peer-urls http://10.217.211.130:2380 \
  --listen-client-urls http://10.217.211.130:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.217.211.130:2379 \
  --initial-cluster-token etcd-cluster-2 \
  --initial-cluster infra1=http://10.217.211.130:2380 \
  --initial-cluster-state new

etcdctl member add infra2 --peer-urls=http://10.221.50.14:2380

NODE 2
------
etcd --name infra2 --initial-advertise-peer-urls http://10.221.50.14:2380 \
  --listen-peer-urls http://10.221.50.14:2380 \
  --listen-client-urls http://10.221.50.14:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.221.50.14:2379 \
  --initial-cluster-token etcd-cluster-2 \
  --initial-cluster infra1=http://10.217.211.130:2380,infra2=http://10.221.50.14:2380 \
  --initial-cluster-state existing

etcdctl member add infra3 --peer-urls=http://10.217.202.140:2380


NODE 3
------
etcd --name infra3 --initial-advertise-peer-urls http://10.217.202.140:2380 \
  --listen-peer-urls http://10.217.202.140:2380 \
  --listen-client-urls http://10.217.202.140:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.217.202.140:2379 \
  --initial-cluster-token etcd-cluster-2 \
  --initial-cluster infra1=http://10.217.211.130:2380,infra3=http://10.217.202.140:2380,infra2=http://10.221.50.14:2380 \
  --initial-cluster-state existing


