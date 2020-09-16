#!/bin/bash

A=$1
if [[ -z "$A" ]]; then
    echo "Missing global accelerator. Try again"
    exit 0
fi
A="http://${A}"
STR=""
for i in .data/i.*;
do
    STR=" -i $i"
    echo Querying client: $i
    echo Responding Server `ansible-playbook $STR test-ansible.yml --extra-vars "GAURL=$A" | grep showzone`

done
