#!/bin/bash

export ANSIBLE_HOST_KEY_CHECKING=False

function begin ()
{
    terraform apply -auto-approve

    TF_STATE=. ansible-playbook --inventory-file=$(which terraform-inventory) test-ansible.yml
}

function end ()
{
    terraform destroy -auto-approve
}

while [ $# -gt 0 ]
do
    case $1 in
        -v|--verbose) set -x ;;
        -b|--begin|--start)
                begin
                ;;
        -e|--end|--stop)
                end
                ;;
        --restart)
                end;
                begin;
                ;;
        (*) break;;
    esac
  shift
done

