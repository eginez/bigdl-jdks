#!/bin/bash
## $1 first parameter ip address
## $2 batch size
## $3 name of out file
## $4 config file json file


ssh -o StrictHostKeyChecking=no $1 mkdir -p /tmp/ml_scripts
scp lenet5.py  $1:/tmp/ml_scripts
## Copy generated conf.json
scp /home/shrey/bigdl-jdks/infra/conf.json  $1:/tmp/ml_scripts
## TODO add more setup steps

mkdir -p results
ssh -o StrictHostKeyChecking=no $1 cat /tmp/ml_scripts/conf.json
ssh -o StrictHostKeyChecking=no $1 /home/am72ghiassi/bd/sparkgen-bigdl/src/sparkgen/sparkgen -r -d -c /tmp/ml_scripts/conf.json > results/measurements.txt
python3 parse_log.py -l results/measurements.txt -m results/$3.csv

scp -R $1:/home/shrey/test /python_results/
#when running more than two workloads
#scp $1:/home/am72ghiassi/bd/sparkgen-bigdl/src/sparkgen/result1.csv results1/$3.csv
gsutil cp results/$3.csv gs://qpecs-output/queue
