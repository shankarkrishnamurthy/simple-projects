Author:
    Shankar,K
Date:
    2019
Description:
  This uses fedora images.
  Run following cmds. Some can be parallelized. But, for now, no interest.
  creation:
     ansible-playbook aws-vpx-1nic.yaml
     ansible-playbook create-master-node.yml # check /etc/ansible/hosts
     ansible-playbook create-worker-node.yml # check /etc/ansible/hosts
     ansible-playbook configure-master-node.yml # check worker-join.cmd
     ansible-playbook configure-worker-node.yml 
     ansible-playbook check-cluster.yml # check output
  deletion:
     ansible-playbook create-master-node.yml -e '{ "undo": true }'
     ansible-playbook create-worker-node.yml -e '{ "undo": true }'
     ansible-playbook aws-vpx-1nic.yaml -e '{ "undo": true }'

  kubeadm notes:

    installation one-time:
        modprobe br_netfilter
        cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
        net.bridge.bridge-nf-call-ip6tables = 1
        net.bridge.bridge-nf-call-iptables = 1
        EOF
        sudo sysctl --system
        /boot/grub2/grubenv <-- systemd.unified_cgroup_hierarchy=0 in kernelopts=

cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-\$basearch
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
exclude=kubelet kubeadm kubectl
EOF
        # Set SELinux in permissive mode (effectively disabling it)
        sudo setenforce 0
        sudo sed -i 's/^SELINUX=enforcing$/SELINUX=disabled/' /etc/selinux/config
        sudo yum install -y kubelet kubeadm kubectl --disableexcludes=kubernetes
        sudo systemctl enable --now kubelet
        dnf install -y kubernetes-cni docker
        sudo systemctl enable docker
        *make sure  kubelet service works. journalctl -xeu kubelet*

        useradd kubeadmin 
        mkdir -p $HOME/.kube
        sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
        sudo chown $(id -u):$(id -g) $HOME/.kube/config

        export KUBECONFIG=/etc/kubernetes/admin.conf [for root]

        / # [root@ip-172-31-0-160 ~]# cat > /etc/systemd/network/50-flannel.link
        [Match]
        OriginalName=flannel*
        [Link]
        MACAddressPolicy=none

        reboot
        
        installation on master (repeatable after cleanup):
        kubeadm init --pod-network-cidr=10.244.0.0/16
        https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml # flannel. CIDR should be same as above
        https://docs.projectcalico.org/manifests/calico.yaml # calico
        # pass --kubelet-insecure-tls if below didn't work. https://github.com/kubernetes-sigs/metrics-server
        kubectl apply -f \
          https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

        kubectl get all 
        [root@ip-172-31-11-235 ~]# kubeadm token create --print-join-command

        worker node join:
        kubeadm join 172.31.11.235:6443 --token 3dt5kh.y86r50u34dypcsul --discovery-token-ca-cert-hash sha256:37c9ba776d18f020b6f596c9e24287c1aa15456e4b1121e5d0b658ae8e724cc6 # output of 'kubeadm token create --print-join-command'

        steps full cleanup:
        kubectl delete --all daemonset
        kubectl delete --all deployment
        kubectl delete -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml 
        #kubectl delete -f https://docs.projectcalico.org/manifests/calico.yaml # for calico
        #kubectl delete -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml # for metrics server

        sudo kubeadm reset -f && 
        sudo systemctl stop kubelet && 
        sudo systemctl stop docker && 
        sudo rm -rf /var/lib/cni/ && 
        sudo rm -rf /var/lib/kubelet/* && 
        sudo rm -rf /etc/cni/ && 
        sudo ifconfig cni0 down && 
        sudo ifconfig flannel.1 down && 
        sudo ifconfig docker0 down && 
        sudo ip link delete cni0 && 
        sudo ip link delete flannel.1
    
        steps remove a node:
        kubectl get nodes
        kubectl drain <node-name>
        kubectl uncordon <node> #opposite of drain
        kubectl drain <node-name> --ignore-daemonsets --delete-local-data
        kubectl delete node <node-name>
        kubeadm reset 

        steps to clean pods:
        kubectl delete pod --all --grace-period=0 --force # if in terminating condition

        steps scaling:
        "imagePullPolicy: IfNotPresenta" in pod yaml
        /etc/sysconfig/kubelet -> KUBELET_EXTRA_ARGS="--max-pods=250"
        
        steps test:
        kubectl run -i --tty --rm debug --image=busybox --restart=Never -- sh

        steps to change EKS CNI (to calico):
            kubectl delete daemonset -n kube-system aws-node
            kubectl apply -f https://docs.projectcalico.org/manifests/calico-vxlan.yaml
            eksctl create nodegroup --cluster my-calico-cluster --node-type t3.medium --node-ami auto --max-pods-per-node 300
            
        references:
        https://github.com/ravdy/kubernetes/blob/master/Kubernetes_Setup_using_kubeadm.md
        https://www.youtube.com/watch?v=wgbpEqyjFoY
        https://www.youtube.com/watch?v=E3h8_MJmkVU&t=423s
        https://www.youtube.com/watch?v=QZ3PQozmfFM
        https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/
        https://www.praqma.com/stories/debugging-kubernetes-networking/
                

