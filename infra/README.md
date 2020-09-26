- Create a driver image with privileges to create infra
- run the install-tf.sh `bash install-tf.sh`
- You know have a master to run experiments, you can see the ui in http://ip_address:8080/, where ip_address is the external ip address.
- there is runlenet.sh file you can use to try stuff
  ```
    scp ../runlenet.sh [ip_address_of_master]:~/
    ssh [ip_address_of_master] bash ~/runlenet.sh ip_address_of_master
  ```
