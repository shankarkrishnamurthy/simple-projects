#!/bin/env bash

# Run App 1
D1=$(docker run -d --rm -v $PWD:/var/log/ --entrypoint bash bash -c 'CNT=0;while true;do echo $(date +%x:%T) $CNT Hello-app-1 $(head -c 10 /dev/urandom | base64 ) >> /var/log/myapp-1.log; CNT=$((CNT+1));sleep 1;done')

# Run App 2
D2=$(docker run -d --rm -v $PWD:/var/log/ --entrypoint bash bash -c 'CNT=0;while true;do echo $(date +%x:%T) $CNT Hello-app-2 $(head -c 10 /dev/urandom | base64 ) >> /var/log/myapp-2.log; CNT=$((CNT+1));sleep 1;done')

# Run Fluentd
D3=$(docker run -d --rm -p 9880:9880 -v $PWD:/tmp -v $PWD:/fluentd/etc -e FLUENTD_CONF=fluentd.conf fluent/fluentd)


function clean ()
{
    docker stop $D3 $D1 $D2
    rm -rf *log *pos
    exit 0
}
trap clean INT TERM

while true;
do
  echo tail -f combine-json.log/buffer*log
  sleep 1
done
