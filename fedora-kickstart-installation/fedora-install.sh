#!/bin/bash
# 
# Description:
#       Simple script which takes live fedora ISO and creates a VM
#   without manual intervention
#
#   Step 1: create a minimalist disk. Loop mount it
#   Step 2: create kickstart with minimal config
#   Step 3: invoke anaconda on this kickstart
#   Step 4: Run virt-install to import this disk
#

if [[ -z "$1" ]]; then
    echo "Give iso to install"
    exit 0
fi
ISO=$1
if [[ ! -e "$ISO" ]]; then
    echo "ISO not found"
    exit 0
fi 
IMG="/var/lib/libvirt/images/f32.img"
VM="fedora31"

virsh shutdown $VM
sleep 10
virsh start $VM
sleep 10

# cleanup
virsh change-media $VM --path sda --eject --live
virsh detach-disk $VM vdb
rm $IMG

#fresh alloc
fallocate -l 25G $IMG;sleep 1
virsh change-media $VM --path sda --source $ISO --insert --live; sleep 1
virsh attach-disk $VM $IMG vdb --cache none

sleep 10 

#
#echo "Run bash -x /root/mnt.sh & bash -x /root/inst.sh in remote"
#read -n 1 -r -s -p $'Press enter once finished ...\n'
ansible all -i '192.168.100.201,' -m shell -a 'bash -x /root/mnt.sh'
ansible all -i '192.168.100.201,' -m shell -a 'bash -x /root/inst.sh'

VMNAME=vm-`cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 8 | head -n 1`
virsh detach-disk $VM vdb
virt-install \
  --name $VMNAME \
  --memory 2048 \
  --vcpus 2 \
  --disk $IMG \
  --os-variant "fedora32"\
  --noautoconsole \
  --import 


