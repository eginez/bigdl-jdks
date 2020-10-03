#!/bin/bash
## $1 first parameter ip address
## $2 batch size
## constraints
## $3 iteration
## $4 validation score
ssh $1 mkdir -p /tmp/ml_scripts
scp lenet5.py  $1:/tmp/ml_scripts
## TODO add more setup steps

ssh $1 /home/am72ghiassi/bd/spark/bin/spark-submit --master spark://$1:7077 --driver-cores 1 --driver-memory 1G --total-executor-cores 2 --executor-cores 1 --executor-memory 1G --py-files /home/am72ghiassi/bd/spark/lib/bigdl-0.11.0-python-api.zip,/tmp/ml_scripts/lenet5.py --properties-file /home/am72ghiassi/bd/spark/conf/spark-bigdl.conf --jars /home/am72ghiassi/bd/spark/lib/bigdl-SPARK_2.3-0.11.0-jar-with-dependencies.jar --conf spark.driver.extraClassPath=/home/am72ghiassi/bd/spark/lib/bigdl-SPARK_2.3-0.11.0-jar-with-dependencies.jar --conf spark.executer.extraClassPath=bigdl-SPARK_2.3-0.11.0-jar-with-dependencies.jar  /tmp/ml_scripts/lenet5.py --action train --dataPath /tmp/mnist -b $2 -i $3 -s $4
