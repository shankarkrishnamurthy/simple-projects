#!/bin/bash
A=$1
if [[ -z "$A" ]]; then
    echo "missing action param. try again"
    exit 0
fi
REG="ap-south-1 sa-east-1"

#terraform init
mkdir -p .data
#REG=$(aws ec2 describe-regions --region-names --output text | tr "\t" " " | cut -f4 -d" ")
for i in $REG; do
    echo "Region: $i"
    echo "region=\"$i\"" > terraform.tfvars
    if [[ -e  ".data/terraform.tfstate.$i" ]]; then
        cp  .data/terraform.tfstate.$i  terraform.tfstate
    fi

    terraform $A --auto-approve

    if [[ "$A" != "destroy" ]]; then
        cp terraform.tfstate .data/terraform.tfstate.$i
        TF_STATE=. terraform-inventory --inventory > .data/i.$i
    fi
done

if [[ "$A" == "destroy" ]]; then
    rm -f terraform.tfstate* .data/*
fi


