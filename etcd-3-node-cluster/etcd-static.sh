NODE1 (infra0)
--------------
etcd --name infra0 --initial-advertise-peer-urls http://10.217.202.38:2380 \
  --listen-peer-urls http://10.217.202.38:2380 \
  --listen-client-urls http://10.217.202.38:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.217.202.38:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=http://10.217.202.38:2380,infra1=http://10.217.202.140:2380,infra2=http://10.221.50.14:2380 \
  --initial-cluster-state new

NODE2 (infra2)
--------------
etcd --name infra2 --initial-advertise-peer-urls http://10.221.50.14:2380 \
  --listen-peer-urls http://10.221.50.14:2380 \
  --listen-client-urls http://10.221.50.14:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.221.50.14:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=http://10.217.202.38:2380,infra1=http://10.217.202.140:2380,infra2=http://10.221.50.14:2380 \
  --initial-cluster-state new

NODE3 (infra1)
--------------
etcd --name infra1 --initial-advertise-peer-urls http://10.217.202.140:2380 \
  --listen-peer-urls http://10.217.202.140:2380 \
  --listen-client-urls http://10.217.202.140:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.217.202.140:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=http://10.217.202.38:2380,infra1=http://10.217.202.140:2380,infra2=http://10.221.50.14:2380 \
  --initial-cluster-state new


