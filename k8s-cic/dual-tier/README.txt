steps:
kubectl apply -f namespace.yaml 
kubectl apply -f frontend-developers-secret.yaml -n frontend-developers
kubectl apply -f frontend-developers-app.yaml -n frontend-developers
kubectl apply -f frontend-developers-rbac.yaml -n frontend-developers
kubectl create secret generic nslogin --from-literal=username='nsroot' --from-literal=password='nsroot' -n frontend-developers
kubectl apply -f frontend-developers-cpx.yaml -n frontend-developers
kubectl apply -f frontend-developers-cic.yaml -n frontend-developers  #!modify NSIP!
kubectl apply -f frontend-developers-ingress.yaml -n frontend-developers  #!check frontend-ip!

cleanup:
kubectl delete -f frontend-developers-ingress.yaml -n frontend-developers # !check frontend-ip!
kubectl delete -f frontend-developers-cic.yaml -n frontend-developers # !modify NSIP!
kubectl delete -f frontend-developers-cpx.yaml -n frontend-developers
kubectl delete secret nslogin -n frontend-developers
kubectl delete -f frontend-developers-rbac.yaml -n frontend-developers
kubectl delete -f frontend-developers-app.yaml -n frontend-developers
kubectl delete -f frontend-developers-secret.yaml -n frontend-developers
kubectl delete -f namespace.yaml 

vpx logs:

> show lb vs frontend-ingress-vpx_frontend-developers_443_frontend-lb-service-frontend_frontend-developers_443_svc

	frontend-ingress-vpx_frontend-developers_443_frontend-lb-service-frontend_frontend-developers_443_svc (0.0.0.0:0) - HTTP	Type: ADDRESS 
	State: UP
	Last state change was at Sat Jan 16 05:19:47 2021
	Time since last state change: 0 days, 00:00:23.820
	Effective State: UP  ARP:DISABLED
	Client Idle Timeout: 180 sec
	Down state flush: ENABLED
	Disable Primary Vserver On Down : DISABLED
	Appflow logging: ENABLED
	Port Rewrite : DISABLED
	No. of Bound Services :  1 (Total) 	 1 (Active)
	Configured Method: LEASTCONNECTION
	Current Method: Round Robin, Reason: Bound service's state changed to UP	BackupMethod: ROUNDROBIN
	Mode: IP
	Persistence: NONE
	Vserver IP and Port insertion: OFF 
	Push: DISABLED	Push VServer: 
	Push Multi Clients: NO
	Push Label Rule: none
	L2Conn: OFF
	Skip Persistency: None
	Listen Policy: NONE
	IcmpResponse: PASSIVE
	RHIstate: PASSIVE
	New Service Startup Request Rate: 0 PER_SECOND, Increment Interval: 0
	Mac mode Retain Vlan: DISABLED
	DBS_LB: DISABLED
	Process Local: DISABLED
	Traffic Domain: 0
	TROFS Persistence honored: ENABLED
	Retain Connections on Cluster: NO

Bound Service Groups:
1)	Group Name: frontend-ingress-vpx_frontend-developers_443_frontend-lb-service-frontend_frontend-developers_443_svc

		1) frontend-ingress-vpx_frontend-developers_443_frontend-lb-service-frontend_frontend-developers_443_svc (10.244.2.29: 443) - SSL State: UP	Weight: 1
 Done
> stat lb vs

Virtual Server(s) Summary
                      vsvrIP  port     Protocol        State    Req/s   CPU-PM 
fron...3_svc         0.0.0.0     0         HTTP           UP      2/s        0

 Done
> stat csvs

Vserver(s) Summary
                          IP  port     Protocol        State    Req/s 
fron...3_ssl     172.31.3.21   443          SSL           UP      0/s

 Done
> show servicegroup frontend-ingress-vpx_frontend-developers_443_frontend-lb-service-frontend_frontend-developers_443_svc
	frontend-ingress-vpx_frontend-developers_443_frontend-lb-service-frontend_frontend-developers_443_svc - SSL
	State: ENABLED	Effective State: UP	Monitor Threshold : 0
	Max Conn: 0	Max Req: 0	Max Bandwidth: 0 kbits
	Use Source IP: NO	
	Client Keepalive(CKA): NO
	Monitoring Owner: 0
	TCP Buffering(TCPB): NO
	HTTP Compression(CMP): NO
	Idle timeout: Client: 180 sec	Server: 360 sec
	Client IP: DISABLED 
	Cacheable: NO
	SC: OFF
	SP: OFF
	Down state flush: ENABLED
	Monitor Connection Close : NONE
	Appflow logging: ENABLED
	ContentInspection profile name: ???
	Process Local: DISABLED
	Traffic Domain: 0


	1)     10.244.2.29:443	State: UP	Server Name: 10.244.2.29	Server ID: None	Weight: 1
		Last state change was at Sat Jan 16 05:19:47 2021 
		Time since last state change: 0 days, 00:01:00.240

		Monitor Name: tcp-default 	State: UP	Passive: 0
		Probes: 23	Failed [Total: 12 Current: 0]
		Last response: Success - TCP syn+ack received.
		Response Time: 0 millisec
 Done

cpx logs:

root@cpx-ingress-55d68b846-h8vwm:/# cli_script.sh "show lb vs k8s-frontend-ingress_frontend-developers_443_k8s-frontend-developers_frontend-developers_443_svc"
exec: show lb vs k8s-frontend-ingress_frontend-developers_443_k8s-frontend-developers_frontend-developers_443_svc
	k8s-frontend-ingress_frontend-developers_443_k8s-frontend-developers_frontend-developers_443_svc (0.0.0.0:0) - TCP	Type: ADDRESS 
	State: UP
	Last state change was at Sat Jan 16 05:15:53 2021
	Time since last state change: 0 days, 00:07:07.20
	Effective State: UP  ARP:DISABLED
	Client Idle Timeout: 9000 sec
	Down state flush: ENABLED
	Disable Primary Vserver On Down : DISABLED
	Appflow logging: ENABLED
	No. of Bound Services :  2 (Total) 	 2 (Active)
	Configured Method: LEASTCONNECTION
	Current Method: Round Robin, Reason: Bound service's state changed to UP	BackupMethod: ROUNDROBIN
	Mode: IP
	Persistence: NONE
	Connection Failover: DISABLED
	L2Conn: OFF
	Skip Persistency: None
	Listen Policy: NONE
	IcmpResponse: PASSIVE
	RHIstate: PASSIVE
	New Service Startup Request Rate: 0 PER_SECOND, Increment Interval: 0
	Mac mode Retain Vlan: DISABLED
	DBS_LB: DISABLED
	Process Local: DISABLED
	Traffic Domain: 0
	TROFS Persistence honored: ENABLED
	Retain Connections on Cluster: NO
Bound Service Groups:
1)	Group Name: k8s-frontend-ingress_frontend-developers_443_k8s-frontend-developers_frontend-developers_443_svc
		1) k8s-frontend-ingress_frontend-developers_443_k8s-frontend-developers_frontend-developers_443_svc (10.244.2.27: 443) - SSL_TCP State: UP	Weight: 1
		2) k8s-frontend-ingress_frontend-developers_443_k8s-frontend-developers_frontend-developers_443_svc (10.244.2.28: 443) - SSL_TCP State: UP	Weight: 1
5)	CSPolicy: 	CSVserver: k8s-10.244.2.29_443_ssl_tcp	Priority: 0	Hits: 3
Done
root@cpx-ingress-55d68b846-h8vwm:/# cli_script.sh "show servicegroup k8s-frontend-ingress_frontend-developers_443_k8s-frontend-developers_frontend-developers_443_svc"
exec: show servicegroup k8s-frontend-ingress_frontend-developers_443_k8s-frontend-developers_frontend-developers_443_svc
	k8s-frontend-ingress_frontend-developers_443_k8s-frontend-developers_frontend-developers_443_svc - SSL_TCP
	State: ENABLED	Effective State: UP	Monitor Threshold : 0
	Max Conn: 0	Max Req: 0	Max Bandwidth: 0 kbits
	Use Source IP: NO	
	Client Keepalive(CKA): NO
	Monitoring Owner: 0
	TCP Buffering(TCPB): NO
	HTTP Compression(CMP): NO
	Idle timeout: Client: 9000 sec	Server: 9000 sec
	Client IP: DISABLED 
	Cacheable: NO
	SC: OFF
	SP: OFF
	Down state flush: ENABLED
	Monitor Connection Close : NONE
	Appflow logging: ENABLED
	ContentInspection profile name: ???
	Process Local: DISABLED
	Traffic Domain: 0

	1)     10.244.2.27:443	State: UP	Server Name: 10.244.2.27	Server ID: None	Weight: 1
		Last state change was at Sat Jan 16 05:15:53 2021 
		Time since last state change: 0 days, 00:07:28.460
		Monitor Name: tcp-default 	State: UP	Passive: 0
		%Probes: 86	Failed [Total: 0 Current: 0]
		Last response: Success - TCP syn+ack received.
		Response Time: 0 millisec
	2)     10.244.2.28:443	State: UP	Server Name: 10.244.2.28	Server ID: None	Weight: 1
		Last state change was at Sat Jan 16 05:15:53 2021 
		Time since last state change: 0 days, 00:07:28.470
		Monitor Name: tcp-default 	State: UP	Passive: 0
		%Probes: 85	Failed [Total: 0 Current: 0]
		Last response: Success - TCP syn+ack received.
		Response Time: 0 millisec
Done

[root@ip-172-31-1-32 ~]# kubectl get pods -A -o wide
NAMESPACE             NAME                                                                READY   STATUS    RESTARTS   AGE     IP             NODE                                         NOMINATED NODE   READINESS GATES
frontend-developers   cic-vpx                                                             1/1     Running   0          7m43s   10.244.2.30    ip-172-31-9-120.us-west-1.compute.internal   <none>           <none>
frontend-developers   cpx-ingress-55d68b846-h8vwm                                         2/2     Running   0          8m8s    10.244.2.29    ip-172-31-9-120.us-west-1.compute.internal   <none>           <none>
frontend-developers   frontend-developers-589658746b-ws9tt                                1/1     Running   0          8m9s    10.244.2.28    ip-172-31-9-120.us-west-1.compute.internal   <none>           <none>
frontend-developers   frontend-developers-589658746b-zbjrg                                1/1     Running   0          8m9s    10.244.2.27    ip-172-31-9-120.us-west-1.compute.internal   <none>           <none>
kube-system           coredns-74ff55c5b-ph8sb                                             1/1     Running   0          9h      10.244.0.2     ip-172-31-1-32.us-west-1.compute.internal    <none>           <none>
kube-system           coredns-74ff55c5b-v5dvz                                             1/1     Running   0          9h      10.244.0.3     ip-172-31-1-32.us-west-1.compute.internal    <none>           <none>
kube-system           etcd-ip-172-31-1-32.us-west-1.compute.internal                      1/1     Running   0          9h      172.31.1.32    ip-172-31-1-32.us-west-1.compute.internal    <none>           <none>
kube-system           kube-apiserver-ip-172-31-1-32.us-west-1.compute.internal            1/1     Running   0          9h      172.31.1.32    ip-172-31-1-32.us-west-1.compute.internal    <none>           <none>
kube-system           kube-controller-manager-ip-172-31-1-32.us-west-1.compute.internal   1/1     Running   0          9h      172.31.1.32    ip-172-31-1-32.us-west-1.compute.internal    <none>           <none>
kube-system           kube-flannel-ds-njmmr                                               1/1     Running   0          8h      172.31.9.120   ip-172-31-9-120.us-west-1.compute.internal   <none>           <none>
kube-system           kube-flannel-ds-p7rh4                                               1/1     Running   0          9h      172.31.1.32    ip-172-31-1-32.us-west-1.compute.internal    <none>           <none>
kube-system           kube-proxy-48tzk                                                    1/1     Running   0          8h      172.31.9.120   ip-172-31-9-120.us-west-1.compute.internal   <none>           <none>
kube-system           kube-proxy-gg7gq                                                    1/1     Running   0          9h      172.31.1.32    ip-172-31-1-32.us-west-1.compute.internal    <none>           <none>
kube-system           kube-scheduler-ip-172-31-1-32.us-west-1.compute.internal            1/1     Running   0          9h      172.31.1.32    ip-172-31-1-32.us-west-1.compute.internal    <none>           <none>

