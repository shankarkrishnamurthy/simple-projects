#!/bin/env bash

set -e
set -x
VER=29

function cleanup {
    echo "Fedora Upgrade to Fedora-${VER} Failed"
    set +x
}
trap cleanup EXIT


dnf upgrade --refresh -y

dnf install -y dnf-plugin-system-upgrade

dnf system-upgrade -y --refresh --releasever=${VER} --allowerasing download

dnf system-upgrade -y reboot
