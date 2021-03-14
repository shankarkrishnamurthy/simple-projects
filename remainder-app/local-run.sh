#!/bin/env bash

ARG=$1
if [[ -n "$ARG" && "$ARG" == "stop" ]]; then
    pgrep gunicorn | xargs kill -9
    docker stop postgres
else # start
    LOGFILE=rapp.log
    rm $LOGFILE
    #postgresql
    docker run --rm -it -p 5432:5432 --name postgres -e POSTGRES_PASSWORD=mysecret -v $(pwd)/postgres-data:/var/lib/postgresql/data -d postgres
    # Start app
    gunicorn -b :5000 --daemon --reload --log-file $LOGFILE --capture-output app:app
fi
