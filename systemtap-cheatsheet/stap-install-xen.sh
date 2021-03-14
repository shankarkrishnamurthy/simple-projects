#!/bin/bash

set -e

DNS=10.216.4.21
LOCN=/media
TGT=/usr/lib/debug
if [[ -e "${TGT}/.debuginfo" ]]; then
    echo "already debuginfo mounted"
else
    P=$($LOCN/xendisk.sh)
    [[ -z "$P" ]] && die "xendisk doesn't exists"
    mkfs.ext3 $P
    [[ -e "$TGT" ]] && mv $TGT ${TGT}.orig
    mkdir -p $TGT
    mount $P $TGT
fi

cat << EOF >> /etc/resolv.conf
nameserver $DNS
EOF
yum install --enablerepo=base -y gcc
yum install --enablerepo=base -y systemtap-client systemtap-runtime

[[ -e "${TGT}/.debuginfo" ]] || rpm -Uvh $LOCN/kernel-de*rpm --force
touch $TGT/.debuginfo
rpm -qa | grep -q systemtap-devel || rpm -ivh $LOCN/systemtap-devel-*.rpm --nodeps

# Final Test
stap -k -v -e 'probe vfs.read {printf("read performed\n"); exit()}'

