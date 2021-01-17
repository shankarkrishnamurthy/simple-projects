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
