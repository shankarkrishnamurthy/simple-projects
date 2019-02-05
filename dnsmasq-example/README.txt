dnsmasq can be used for both DNS resolution AND DHCP server
------------------------------------------------------------

For dnsmasq using linux network namespace, refer <dnsmasq-in-linux-namespace.sh>
Here dnsmasq is demonstrated using VMs


dnsmasq as DNS
---------------

step 1:
-------
cp /etc/dnsmasq.conf/dns /etc/dnsmasq.conf
service dnsmasq restart

[root@zela-f29 dnsmasq-example]# cat /etc/hosts
127.0.0.1	localhost
::1		localhost6.localdomain6 localhost6

10.217.202.140 dev.linuxarium.com
10.217.211.130 zela-f29
10.217.202.140 galata-fc28
10.221.50.14   abacus-fc28
[root@zela-f29 dnsmasq-exa

Step 2:
-------
[root@zela-f29 ~]# rm /etc/resolv.conf

***TEST**
---------

[root@zela-f29 ~]# nslookup abacus-fc28
Server:		127.0.0.1
Address:	127.0.0.1#53

Name:	abacus-fc28
Address: 10.221.50.14

[root@zela-f29 ~]# dig abacus-fc28

; <<>> DiG 9.11.4-P2-RedHat-9.11.4-10.P2.fc29 <<>> abacus-fc28
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 31108
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;abacus-fc28.			IN	A

;; ANSWER SECTION:
abacus-fc28.		0	IN	A	10.221.50.14

;; Query time: 0 msec
;; SERVER: 127.0.0.1#53(127.0.0.1)
;; WHEN: Mon Jan 21 17:15:16 PST 2019
;; MSG SIZE  rcvd: 56

[root@zela-f29 ~]# dig abacus-fc28.my-lab.net

; <<>> DiG 9.11.4-P2-RedHat-9.11.4-10.P2.fc29 <<>> abacus-fc28.my-lab.net
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 50474
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;abacus-fc28.my-lab.net.		IN	A

;; ANSWER SECTION:
abacus-fc28.my-lab.net.	0	IN	A	10.221.50.14

;; Query time: 0 msec
;; SERVER: 127.0.0.1#53(127.0.0.1)
;; WHEN: Mon Jan 21 17:15:28 PST 2019
;; MSG SIZE  rcvd: 67

[root@zela-f29 ~]#


dnsmasq as DHCP server
-----------------------

cp /etc/dnsmasq.conf.dhcp /etc/dnsmasq.conf

service dnsmasq restart

**TEST**
--------

0. CREATE localbr
1. START VM with localbr bridge
2. dhclient ens3


[root@zela-f29 dnsmasq-example]# ifconfig localbr
localbr: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 11.11.0.1  netmask 255.255.255.0  broadcast 11.11.0.255
        inet6 fe80::ac80:5cff:fe1e:ea42  prefixlen 64  scopeid 0x20<link>
        ether f6:38:67:df:79:49  txqueuelen 1000  (Ethernet)
        RX packets 168  bytes 20556 (20.0 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 378  bytes 24600 (24.0 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

INSIDE VM
---------
[root@fedora-26-vm ~]# ifconfig ens3
ens3: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 11.11.0.74  netmask 255.255.255.0  broadcast 11.11.0.255
        inet6 fe80::233c:5040:8779:78a5  prefixlen 64  scopeid 0x20<link>
        ether 52:54:00:da:06:48  txqueuelen 1000  (Ethernet)
        RX packets 575  bytes 34325 (33.5 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 159  bytes 22706 (22.1 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0


