Tier 1:

    Create VPX:
        https://github.com/citrix/citrix-adc-aws-cloudformation/tree/master/templates/standalone (1_nic)
    Create Cluster:
        https://github.com/shankarkrishnamurthy/simple-projects/tree/master/k8s-cluster-setup-aws
    create test m/c:
        https://github.com/shankarkrishnamurthy/simple-projects/tree/master/terraform-ansible-aws
        *orchestrate.sh -s*
    Download yaml(s):
        https://github.com/citrix/cloud-native-getting-started/tree/master/on-prem/Unified-Ingress
    commands:
        kubectl create namespace tier-2-adc
        kubectl apply -f rbac.yaml 
        kubectl apply -f colddrink.yaml -n tier-2-adc
        kubectl apply -f ipam-crd.yaml 
        kubectl apply -f ipam.yaml  # !modify VIP_RANGE!
        kubectl apply -f tier-1-cic.yaml -n tier-2-adc # !modify NS_IP/LOGIN/PASSWD!

    verify:
[root@ip-172-31-13-7 ~]# kubectl get svc -n tier-2-adc -o wide
NAME                  TYPE           CLUSTER-IP      EXTERNAL-IP    PORT(S)                      AGE   SELECTOR
frontend-colddrinks   LoadBalancer   10.108.113.36   *172.31.3.132*   80:30870/TCP,443:31133/TCP   55m   app=frontend-colddrinks

    rules created in ADC:
add serviceGroup k8s150-frontend-colddrinks_tier-2-adc_80_svc_k8s150-frontend-colddrinks_tier-2-adc_80_svc TCP -maxClient 0 -maxReq 0 -cip DISABLED -usip NO -useproxyport YES -cltTimeout 9000 -svrTimeout 9000 -CKA NO -TCPB NO -CMP NO
add lb vserver k8s150-frontend-colddrinks_tier-2-adc_80_svc_k8s150-frontend-colddrinks_tier-2-adc_80_svc TCP 0.0.0.0 0 -persistenceType NONE -cltTimeout 9000
add cs vserver k8s150-frontend-colddrinks_tier-2-adc_80_svc TCP 172.31.13.4 80 -cltTimeout 9000 -comment uid=6M4EFZKL3EINK4RP4PNJ4LTOVSDGU75XGE23N5MGLC677BXDUGEA==== -persistenceType NONE
bind lb vserver k8s150-frontend-colddrinks_tier-2-adc_80_svc_k8s150-frontend-colddrinks_tier-2-adc_80_svc k8s150-frontend-colddrinks_tier-2-adc_80_svc_k8s150-frontend-colddrinks_tier-2-adc_80_svc
bind cs vserver k8s150-frontend-colddrinks_tier-2-adc_80_svc -lbvserver k8s150-frontend-colddrinks_tier-2-adc_80_svc_k8s150-frontend-colddrinks_tier-2-adc_80_svc
bind serviceGroup k8s150-frontend-colddrinks_tier-2-adc_80_svc_k8s150-frontend-colddrinks_tier-2-adc_80_svc 172.31.14.49 30276
            
        cleanup:
        kubectl delete -f tier-1-cic.yaml -n tier-2-adc # !modify NS_IP/LOGIN/PASSWD!
        kubectl delete -f ipam.yaml  # !modify VIP_RANGE!
        kubectl delete -f ipam-crd.yaml 
        kubectl delete -f colddrink.yaml -n tier-2-adc
        kubectl delete -f rbac.yaml 

 

