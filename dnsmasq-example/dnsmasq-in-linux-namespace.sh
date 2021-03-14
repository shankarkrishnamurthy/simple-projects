:<<'COMMENT'

https://www.youtube.com/watch?v=_WgUwUf1d34

Description:

Test 1:
Create red and green namespace. 
Create a veth pair and add one end of the pair to 'red' ns and another end to ovs local bridge
Similarly for green ns. Now set ip to interfaces inside each ns and ping! 

Test 2:
Delete the ip assigned in test 1)
Now create 2 'internal' ovs port in the same bridge.
Also create 2 new network namespace.
Tag the 2 new ports to VLAN 100 and 200. Same with previous eth pair correspondingly.
Essentially there is two isolated network VLAN 100 and 200 respectively.
Run 'dnsmasq' with identical IP address(10.10.10.2) on these two different network.
Now run 'dhclient eth-r' on the  veth end of the network to get dynamic IP address assigned!
All Set

COMMENT

# =====================================
# TEST 1
# =====================================

ip netns add red
ip netns add green
ls -l /var/run/netns/
ip netns exec red ip link
ip netns exec green ip link
#(or)
#ip netns exec green bash
#> ip link
#<exit>

ovs-vsctl add-br ovs1
ovs-vsctl show

ip link add eth-r type veth peer name veth-r
ip link set eth-r netns red
ip netns exec red ip link
ovs-vsctl add-port ovs1 veth-r
ovs-vsctl show

ip link add eth-g type veth peer name veth-g
ip link set eth-g netns green
ovs-vsctl add-port ovs1 veth-g
ovs-vsctl show

ip link set veth-r up
ip link set veth-g up

ip netns exec red ip link set dev lo up
ip netns exec red ip link set dev eth-r up
ip netns exec red ip addr add 10.10.10.1/24 dev eth-r
ip netns exec red ip link
ip netns exec red ip a

ip netns exec green ip link set dev lo up
ip netns exec green ip link set dev eth-g up
ip netns exec green ip addr add 10.10.10.2/24 dev eth-g
ip netns exec green ip link
ip netns exec green ip a

# =====================================
# TEST 2
# =====================================

ip netns exec green ip addr del 10.10.10.2/24 dev eth-g
ip netns exec red ip addr del 10.10.10.1/24 dev eth-r

ip netns add dhcp-g
ip netns add dhcp-r
ovs-vsctl add-port ovs1 tap-r -- set interface tap-r type=internal
ovs-vsctl set port tap-r tag=100
ovs-vsctl add-port ovs1 tap-g -- set interface tap-g type=internal
ovs-vsctl set port tap-g tag=200
ovs-vsctl show # <-- tap-r still shows in ovs even though ip link doesn't

ip link set tap-r netns dhcp-r
ip link set tap-g netns dhcp-g

ip netns exec dhcp-r ip link set dev lo up
ip netns exec dhcp-r ip link set dev tap-r up
ip netns exec dhcp-r ip addr add 10.10.10.2/24 dev tap-r

ip netns exec dhcp-g ip link set dev lo up
ip netns exec dhcp-g ip link set dev tap-g up
ip netns exec dhcp-g ip addr add 10.10.10.2/24 dev tap-g

ip netns exec dhcp-r dnsmasq --interface=tap-r --dhcp-range=10.10.10.10,10.10.10.100,255.255.255.0 --log-queries --log-dhcp --log-facility=/tmp/dns1.log

ip netns exec dhcp-g dnsmasq --interface=tap-g --dhcp-range=10.10.10.10,10.10.10.100,255.255.255.0 --log-queries --log-dhcp --log-facility=/tmp/dns2.log

ovs-vsctl set port veth-g tag=200
ovs-vsctl set port veth-r tag=100

ip netns exec green dhclient eth0-g
ip netns exec red dhclient eth0-r
ip netns exec red ip a s eth-r
:<<'END'
29: eth-r@if28: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether ee:b5:fa:58:9c:e5 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 10.10.10.22/24 brd 10.10.10.255 scope global dynamic eth-r
       valid_lft 3409sec preferred_lft 3409sec
    inet6 fe80::ecb5:faff:fe58:9ce5/64 scope link 
       valid_lft forever preferred_lft forever
END

ip netns exec green ip a s eth-g
:<<'END'
31: eth-g@if30: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 92:4e:c8:16:c2:50 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 10.10.10.50/24 brd 10.10.10.255 scope global dynamic eth-g
       valid_lft 3261sec preferred_lft 3261sec
    inet6 fe80::904e:c8ff:fe16:c250/64 scope link 
       valid_lft forever preferred_lft forever

END
