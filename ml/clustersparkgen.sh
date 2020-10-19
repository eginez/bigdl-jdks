#!/bin/bash
## $1 first parameter ip address
## $2 batch size
## $3 name of out file
## $4 config file json file


ssh -o StrictHostKeyChecking=no $1 mkdir -p /tmp/ml_scripts
scp lenet5.py  $1:/tmp/ml_scripts
## Copy generated conf.json
scp $4  $1:/tmp/ml_scripts
## TODO add more setup steps

ssh -o StrictHostKeyChecking=no $1 /home/am72ghiassi/bd/sparkgen-bigdl/src/sparkgen/sparkgen -r -d -c /tmp/ml_scripts/conf.json
mkdir -p results
scp $1:/home/am72ghiassi/bd/sparkgen-bigdl/src/sparkgen/result.csv results/$3.csv
#when running more than two workloads
#scp $1:/home/am72ghiassi/bd/sparkgen-bigdl/src/sparkgen/result1.csv results1/$3.csv
gsutil cp results/$3.csv gs://qpecs-output
