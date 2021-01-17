steps:
    creation:
        kubectl apply -f namespace.yaml 
        kubectl create secret generic nslogin --from-literal=username='nsroot' --from-literal=password='nsroot' -n tier-2-adc
        kubectl apply -f rbac.yaml 
        kubectl apply -f cpx.yaml -n tier-2-adc
        kubectl apply -f hotdrink-secret.yaml -n tier-2-adc
        kubectl apply -f team_hotdrink.yaml -n team-hotdrink
        kubectl apply -f hotdrink-secret.yaml -n team-hotdrink
        #kubectl apply -f team_colddrink.yaml -n team-colddrink
        #kubectl apply -f colddrink-secret.yaml -n team-colddrink
        #kubectl apply -f team_guestbook.yaml -n team-guestbook
        kubectl apply -f ingress_vpx.yaml -n tier-2-adc # !modify NS info!
        kubectl apply -f cic_vpx.yaml -n tier-2-adc # !modify NS info!
            
    cleanup:
        kubectl delete -f cic_vpx.yaml -n tier-2-adc # !modify NS info!
        kubectl delete -f ingress_vpx.yaml -n tier-2-adc # !modify NS info!
        #kubectl delete -f team_guestbook.yaml -n team-guestbook
        #kubectl delete -f colddrink-secret.yaml -n team-colddrink
        #kubectl delete -f team_colddrink.yaml -n team-colddrink
        kubectl delete -f hotdrink-secret.yaml -n team-hotdrink
        kubectl delete -f team_hotdrink.yaml -n team-hotdrink
        kubectl delete -f hotdrink-secret.yaml -n tier-2-adc
        kubectl delete -f cpx.yaml -n tier-2-adc
        kubectl delete -f rbac.yaml 
        kubectl delete -f namespace.yaml 
        
*see vpx and cpx logs below*

VPX logs:
> stat lb vs

Virtual Server(s) Summary
                      vsvrIP  port     Protocol        State    Req/s   CPU-PM 
k8s-...3_svc         0.0.0.0     0         HTTP           UP      0/s        0

k8s-...0_svc         0.0.0.0     0         HTTP         DOWN      0/s        0

k8s-...3_svc         0.0.0.0     0         HTTP         DOWN      0/s        0

> show lb vs
1)	k8s-ingress-vpx_tier-2-adc_443_k8s-lb-service-hotdrinks_tier-2-adc_443_svc (0.0.0.0:0) - HTTP	Type: ADDRESS 
	State: UP
	Last state change was at Fri Jan 15 20:50:22 2021
	Time since last state change: 0 days, 05:49:06.390
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
2)	k8s-ingress-vpx_tier-2-adc_443_k8s-lb-service-guestbook_tier-2-adc_80_svc (0.0.0.0:0) - HTTP	Type: ADDRESS 
	State: DOWN
	Last state change was at Fri Jan 15 20:50:22 2021
	Time since last state change: 0 days, 05:49:06.380
	Effective State: DOWN  ARP:DISABLED
	Client Idle Timeout: 180 sec
	Down state flush: ENABLED
	Disable Primary Vserver On Down : DISABLED
	Appflow logging: ENABLED
	Port Rewrite : DISABLED
	No. of Bound Services :  1 (Total) 	 0 (Active)
	Configured Method: LEASTCONNECTION	BackupMethod: ROUNDROBIN
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
3)	k8s-ingress-vpx_tier-2-adc_443_k8s-lb-service-colddrinks_tier-2-adc_443_svc (0.0.0.0:0) - HTTP	Type: ADDRESS 
	State: DOWN
	Last state change was at Fri Jan 15 20:50:22 2021
	Time since last state change: 0 days, 05:49:06.20
	Effective State: DOWN  ARP:DISABLED
	Client Idle Timeout: 180 sec
	Down state flush: ENABLED
	Disable Primary Vserver On Down : DISABLED
	Appflow logging: ENABLED
	Port Rewrite : DISABLED
	No. of Bound Services :  1 (Total) 	 0 (Active)
	Configured Method: LEASTCONNECTION	BackupMethod: ROUNDROBIN
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
 Done
    
> show servicegroup k8s-ingress-vpx_tier-2-adc_443_k8s-lb-service-hotdrinks_tier-2-adc_443_svc
	k8s-ingress-vpx_tier-2-adc_443_k8s-lb-service-hotdrinks_tier-2-adc_443_svc - SSL
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


	1)    172.31.9.120:30379	State: UP	Server Name: 172.31.9.120	Server ID: None	Weight: 1
		Last state change was at Fri Jan 15 20:50:22 2021 
		Time since last state change: 0 days, 05:49:52.560

		Monitor Name: tcp-default 	State: UP	Passive: 0
		Probes: 4102	Failed [Total: 1 Current: 0]
		Last response: Success - TCP syn+ack received.
		Response Time: 0 millisec
 Done

[root@ip-172-31-1-32 ~]# kubectl get nodes -o wide
NAME                                         STATUS   ROLES                  AGE    VERSION   INTERNAL-IP    EXTERNAL-IP   OS-IMAGE                               KERNEL-VERSION           CONTAINER-RUNTIME
ip-172-31-1-32.us-west-1.compute.internal    Ready    control-plane,master   8h     v1.20.2   172.31.1.32    <none>        Fedora 33 (Cloud Edition Prerelease)   5.8.14-300.fc33.x86_64   docker://19.3.13
ip-172-31-9-120.us-west-1.compute.internal   Ready    <none>                 7h6m   v1.20.2   172.31.9.120   <none>        Fedora 33 (Cloud Edition Prerelease)   5.8.14-300.fc33.x86_64   docker://19.3.13

cpx logs:
root@cpx-ingress-hotdrinks-5c6c77f7cc-mz9lm:/# cli_script.sh "show lb vs"    
exec: show lb vs
1)	cpx_default_dns_vserver (0.0.0.0:0) - DNS	Type: ADDRESS 
	State: UP
	Last state change was at Fri Jan 15 20:49:35 2021
	Time since last state change: 0 days, 06:54:36.780
	Effective State: UP  ARP:DISABLED
	Client Idle Timeout: 120 sec
	Down state flush: ENABLED
	Disable Primary Vserver On Down : DISABLED
	Appflow logging: ENABLED
	No. of Bound Services :  1 (Total) 	 1 (Active)
	Configured Method: LEASTCONNECTION
	Current Method: Round Robin, Reason: Bound service's state changed to UP	BackupMethod: ROUNDROBIN
	Mode: IP
	Persistence: NONE
	L2Conn: OFF
	Skip Persistency: None
	Listen Policy: NONE
	IcmpResponse: PASSIVE
	RHIstate: PASSIVE
	New Service Startup Request Rate: 0 PER_SECOND, Increment Interval: 0
	Mac mode Retain Vlan: DISABLED
	DBS_LB: DISABLED
	DNS64 Synthesis: DISABLED
	Bypass AAAA: NO
	Recursion Available: NO
	Process Local: DISABLED
	Traffic Domain: 0
	TROFS Persistence honored: ENABLED
	Retain Connections on Cluster: NO
2)	cpx_default_dns_tcp_vserver (0.0.0.0:0) - DNS_TCP	Type: ADDRESS 
	State: UP
	Last state change was at Fri Jan 15 20:49:36 2021
	Time since last state change: 0 days, 06:54:35.450
	Effective State: UP  ARP:DISABLED
	Client Idle Timeout: 180 sec
	Down state flush: ENABLED
	Disable Primary Vserver On Down : DISABLED
	Appflow logging: ENABLED
	No. of Bound Services :  1 (Total) 	 1 (Active)
	Configured Method: LEASTCONNECTION
	Current Method: Round Robin, Reason: Bound service's state changed to UP	BackupMethod: ROUNDROBIN
	Mode: IP
	Persistence: NONE
	L2Conn: OFF
	Skip Persistency: None
	Listen Policy: NONE
	IcmpResponse: PASSIVE
	RHIstate: PASSIVE
	New Service Startup Request Rate: 0 PER_SECOND, Increment Interval: 0
	Mac mode Retain Vlan: DISABLED
	DBS_LB: DISABLED
	DNS64 Synthesis: DISABLED
	Bypass AAAA: NO
	Recursion Available: NO
	Process Local: DISABLED
	Traffic Domain: 0
	TROFS Persistence honored: ENABLED
	Retain Connections on Cluster: NO
3)	k8s-hotdrinks-ingress_team-hotdrink_443_k8s-frontend-hotdrinks_team-hotdrink_80_svc (0.0.0.0:0) - HTTP	Type: ADDRESS 
	State: UP
	Last state change was at Fri Jan 15 20:49:55 2021
	Time since last state change: 0 days, 06:54:16.600
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
4)	k8s-hotdrinks-ingress_team-hotdrink_443_k8s-tea-beverage_team-hotdrink_80_svc (0.0.0.0:0) - HTTP	Type: ADDRESS 
	State: UP
	Last state change was at Fri Jan 15 20:49:55 2021
	Time since last state change: 0 days, 06:54:16.460
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
5)	k8s-hotdrinks-ingress_team-hotdrink_443_k8s-coffee-beverage_team-hotdrink_443_svc (0.0.0.0:0) - HTTP	Type: ADDRESS 
	State: UP
	Last state change was at Fri Jan 15 20:49:56 2021
	Time since last state change: 0 days, 06:54:16.320
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
6)	k8s-hotdrinks-ingress_default_443_k8s-frontend-hotdrinks_default_80_svc (0.0.0.0:0) - HTTP	Type: ADDRESS 
	State: UP
	Last state change was at Fri Jan 15 21:37:40 2021
	Time since last state change: 0 days, 06:06:31.950
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
7)	k8s-hotdrinks-ingress_default_443_k8s-tea-beverage_default_80_svc (0.0.0.0:0) - HTTP	Type: ADDRESS 
	State: UP
	Last state change was at Fri Jan 15 21:38:10 2021
	Time since last state change: 0 days, 06:06:01.560
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
8)	k8s-hotdrinks-ingress_default_443_k8s-coffee-beverage_default_443_svc (0.0.0.0:0) - HTTP	Type: ADDRESS 
	State: UP
	Last state change was at Fri Jan 15 21:38:11 2021
	Time since last state change: 0 days, 06:06:00.880
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
Done

Done
root@cpx-ingress-hotdrinks-5c6c77f7cc-mz9lm:/# cli_script.sh "show lb vs cpx_default_dns_vserver"
exec: show lb vs cpx_default_dns_vserver
	cpx_default_dns_vserver (0.0.0.0:0) - DNS	Type: ADDRESS 
	State: UP
	Last state change was at Fri Jan 15 20:49:35 2021
	Time since last state change: 0 days, 06:55:50.570
	Effective State: UP  ARP:DISABLED
	Client Idle Timeout: 120 sec
	Down state flush: ENABLED
	Disable Primary Vserver On Down : DISABLED
	Appflow logging: ENABLED
	No. of Bound Services :  1 (Total) 	 1 (Active)
	Configured Method: LEASTCONNECTION
	Current Method: Round Robin, Reason: Bound service's state changed to UP	BackupMethod: ROUNDROBIN
	Mode: IP
	Persistence: NONE
	L2Conn: OFF
	Skip Persistency: None
	Listen Policy: NONE
	IcmpResponse: PASSIVE
	RHIstate: PASSIVE
	New Service Startup Request Rate: 0 PER_SECOND, Increment Interval: 0
	Mac mode Retain Vlan: DISABLED
	DBS_LB: DISABLED
	DNS64 Synthesis: DISABLED
	Bypass AAAA: NO
	Recursion Available: NO
	Process Local: DISABLED
	Traffic Domain: 0
	TROFS Persistence honored: ENABLED
	Retain Connections on Cluster: NO
Bound Service Groups:
1)	Group Name: cpx_default_dns_servicegroup
		1) cpx_default_dns_servicegroup (10.96.0.10: 53) - DNS State: UP	Weight: 1
Done

root@cpx-ingress-hotdrinks-5c6c77f7cc-mz9lm:/# cli_script.sh "show servicegroup cpx_default_dns_servicegroup"
exec: show servicegroup cpx_default_dns_servicegroup
	cpx_default_dns_servicegroup - DNS
	State: ENABLED	Effective State: UP	Monitor Threshold : 0
	Max Conn: 0	Max Req: 0	Max Bandwidth: 0 kbits
	Use Source IP: NO	
	Client Keepalive(CKA): NO
	Monitoring Owner: 0
	TCP Buffering(TCPB): NO
	HTTP Compression(CMP): NO
	Idle timeout: Client: 120 sec	Server: 120 sec
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
	2) Monitor Name: cpx_default_dns_tcp_monitor	State: ENABLED	Weight: 1	Passive: 0

	1)      10.96.0.10:53	State: UP	Server Name: 10.96.0.10	Server ID: None	Weight: 1
		Last state change was at Fri Jan 15 20:49:35 2021 
		Time since last state change: 0 days, 06:57:07.240
		Monitor Name: cpx_default_dns_tcp_monitor 	State: UP	Passive: 0
		%Probes: 4803	Failed [Total: 3 Current: 0]
		Last response: Success - TCP syn+ack received.
		Response Time: 0 millisec
Done

root@cpx-ingress-hotdrinks-5c6c77f7cc-mz9lm:/# cli_script.sh "show lb vs k8s-hotdrinks-ingress_team-hotdrink_443_k8s-frontend-hotdrinks_team-hotdrink_80_svc"
exec: show lb vs k8s-hotdrinks-ingress_team-hotdrink_443_k8s-frontend-hotdrinks_team-hotdrink_80_svc
	k8s-hotdrinks-ingress_team-hotdrink_443_k8s-frontend-hotdrinks_team-hotdrink_80_svc (0.0.0.0:0) - HTTP	Type: ADDRESS 
	State: UP
	Last state change was at Fri Jan 15 20:49:55 2021
	Time since last state change: 0 days, 06:57:50.100
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
1)	Group Name: k8s-hotdrinks-ingress_team-hotdrink_443_k8s-frontend-hotdrinks_team-hotdrink_80_svc
		1) k8s-hotdrinks-ingress_team-hotdrink_443_k8s-frontend-hotdrinks_team-hotdrink_80_svc (10.244.2.10: 80) - HTTP State: UP	Weight: 1
Done
root@cpx-ingress-hotdrinks-5c6c77f7cc-mz9lm:/# cli_script.sh "show servicegroup k8s-hotdrinks-ingress_team-hotdrink_443_k8s-frontend-hotdrinks_team-hotdrink_80_svc"
exec: show servicegroup k8s-hotdrinks-ingress_team-hotdrink_443_k8s-frontend-hotdrinks_team-hotdrink_80_svc
	k8s-hotdrinks-ingress_team-hotdrink_443_k8s-frontend-hotdrinks_team-hotdrink_80_svc - HTTP
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

	1)     10.244.2.10:80	State: UP	Server Name: 10.244.2.10	Server ID: None	Weight: 1
		Last state change was at Fri Jan 15 20:49:55 2021 
		Time since last state change: 0 days, 06:58:02.630
		Monitor Name: tcp-default 	State: UP	Passive: 0
		%Probes: 4812	Failed [Total: 1 Current: 0]
		Last response: Success - TCP syn+ack received.
		Response Time: 0 millisec
Done

