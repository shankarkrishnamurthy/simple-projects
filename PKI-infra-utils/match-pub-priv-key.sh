#!/bin/bash
#
# Author: Shankar, K
# Description: various ways to check a key pair (pem format)

function method1 ()
{
    FN=$(mktemp)
    echo 'hello' | openssl rsautl -sign -inkey $F1 -keyform PEM -out $FN

    openssl rsautl -verify -pubin -inkey $F2 -in $FN 2>/dev/null >/dev/null
    if [[ $? -eq 0 ]]; then
        echo "The Keys are a pair"
    else
        echo "The Keys are unrelated"
    fi
    rm $FN
}

if [[ $# < 2 ]];then
    echo "Both private and public key are mandatory $#"
    exit 1
fi
F1=$1
F2=$2
method1 $F1 $F2 # F1 = Private F2 = Public
