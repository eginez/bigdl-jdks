- Create a driver image with privileges to create infra
- run the install-tf.sh `bash install-tf.sh`
- run `export TF_VAR_project_id=your_google_project_id` or harcode it in the `master.tf` file
- change the `master.tf` file if you need to modify things
- run `terraform apply` ( and select appropiate values)
- You know have a master to run experiments, you can see the ui in `http://ip_address:8080/`, where ip_address is the external ip address.
  - If you run into broken links replace the ip with the `external ip` of what you are trying to browse.
- there is runlenet.sh file you can use to try stuff
  ```
    scp ../runlenet.sh [ip_address_of_master]:~/
    ssh [ip_address_of_master] bash ~/runlenet.sh ip_address_of_master
  ```
