#!/bin/env bash

set -e
set -x

function cleanup {
    echo "Fedora Upgrade to Fedora-${VER} Failed"
    set +x
}
trap cleanup EXIT
[[ -z "$VER" ]] && echo "Version is empty $VER . Provide one." && exit 0
echo Upgrading to $VER

dnf upgrade --refresh -y

dnf install -y dnf-plugin-system-upgrade

dnf system-upgrade -y --refresh --releasever=${VER} --allowerasing download

dnf system-upgrade -y reboot
