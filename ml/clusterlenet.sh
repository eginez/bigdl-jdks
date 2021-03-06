#!/bin/bash
## $1 ip address of master
## $2 batch size
## $3 output file name

##Preventing ssh key related issues
ssh-keygen -R $1
##Creating folder in master node to store workload
ssh -o StrictHostKeyChecking=no $1 mkdir -p /tmp/ml_scripts
scp lenet5.py  $1:/tmp/ml_scripts
scp utils.py  $1:/tmp/ml_scripts
## Executing the workload
ssh -o StrictHostKeyChecking=no $1 /home/am72ghiassi/bd/spark/bin/spark-submit --master spark://$1:7077 --driver-cores 1 --driver-memory 1G --total-executor-cores 2 --executor-cores 1 --executor-memory 1G --py-files /home/am72ghiassi/bd/spark/lib/bigdl-0.11.0-python-api.zip,/tmp/ml_scripts/lenet5.py --properties-file /home/am72ghiassi/bd/spark/conf/spark-bigdl.conf --jars /home/am72ghiassi/bd/spark/lib/bigdl-SPARK_2.3-0.11.0-jar-with-dependencies.jar --conf spark.driver.extraClassPath=/home/am72ghiassi/bd/spark/lib/bigdl-SPARK_2.3-0.11.0-jar-with-dependencies.jar --conf spark.executer.extraClassPath=bigdl-SPARK_2.3-0.11.0-jar-with-dependencies.jar  /tmp/ml_scripts/lenet5.py --action train --dataPath /tmp/mnist -b $2
##Processing results and storing them in google cloud storage bucket
mkdir -p results
scp $1:result.csv results/$3.csv
gsutil cp results/$3.csv gs://qpecs-output/anova
