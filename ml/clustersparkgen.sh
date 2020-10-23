#!/bin/bash
## $1 first parameter ip address

#moving workload and json configuration to master node
ssh -o StrictHostKeyChecking=no $1 mkdir -p /tmp/ml_scripts
scp bi-rnn.py  $1:/tmp/ml_scripts
scp utils.py  $1:/tmp/ml_scripts
scp /home/shrey/bigdl-jdks/infra/conf.json  $1:/tmp/ml_scripts
