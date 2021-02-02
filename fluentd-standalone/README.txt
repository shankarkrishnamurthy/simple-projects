Description:
    This is standalone fluentd container demostrating very basic functionality of fluentd app
    This scripts runs two different app (a symbolic one at that) and uses the fluentd to 
        1. read input files from 2 different app
        2. Parse them
        3. regexp into Json
        4. send json output to combined file

    apps are just a bash docker image which spews output to stdout/file

Author:
    Shankar, K (Feb 2021)

Execute:
    bash -x run.sh
