#!/bin/bash

mkdir -p ~/ansible/ ~/Downloads/ 
[[ ! -e ~/ansible/ansible ]] && git clone https://github.com/ansible/ansible.git ~/ansible/ansible 
[[ ! -e ~/Downloads/ansidev-env ]] && virtualenv --system-site-packages ~/Downloads/ansidev-env
. ~/Downloads/ansidev-env/bin/activate
. ~/ansible/ansible/hacking/env-setup

cp my_test* ~/ansible/ansible/lib/ansible/modules/

# Run module in command line
cat > /tmp/args.json <<EOF
{
    "ANSIBLE_MODULE_ARGS": {
        "name": "hello",
        "new": true
    }
}
EOF
python -m ansible.modules.my_test /tmp/args.json  | jq '.'

# Run using playbook
ansible-playbook ./testmod.yml

# Testing local modules standalone
# ~/ansible/ansible/hacking/test-module -m  ~/ansible/ansible/lib/ansible/modules/my_test_facts
