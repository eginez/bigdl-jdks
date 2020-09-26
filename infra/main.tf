
## Inputs ssh public key
## GCP project id
## image name
## machine type
## number of nodes
## username for ssh connections
## JDK_NAME

variable "project_id" {
  description = "google project id"
}

provider "google" {
 # credentials = file("CREDENTIALS_FILE.json")
 project     =  "${var.project_id}"
 region      = "europe-west4"
 zone      = "europe-west4-a"
}

data "google_compute_image" "bigdl_custom_image" {
  # Change this to your image name
  name = "bigdl-jdks"
}

variable "num_nodes" {
  description = "Number of nodes to create"
}

variable "jdk_version" {
    description = "set this to the jdk you want to use, only two options $OPENJDK_HOME or $GRAALVM_HOME"
    default = "$OPENJDK_HOME"
}

variable "machine_type" {
  description  = "They type of machine dictates the number of vcpus in it, see: https://cloud.google.com/compute/docs/machine-types#e2_machine_types_beta"
   #e2-highmem-4
   #e2-highmem-8
   #e2-highmem-16" 
  default = "e2-highmem-4" 
}

# user name for ssh key
variable "user" {}

#path to the public key file
variable "ssh_pub" {
    default = "~/.ssh/id_rsa.pub"
}

variable "ssh_priv" {
    default = "~/.ssh/id_rsa"
}

resource "google_compute_instance" "vm_instance_master" {
  name         = "master-instance"
  #machine_type = "${var.machine_type}"
  machine_type = "f1-micro"

  count        = "1"
  allow_stopping_for_update = true

  boot_disk {
    initialize_params {
      # image = "debian-cloud/debian-9"
      image = "${data.google_compute_image.bigdl_custom_image.self_link}"
    }
  }

  network_interface {
    # A default network is created for all GCP projects
    network = "default"
    access_config {
    }
  }

   metadata = {
    ssh-keys = "${var.user}:${file(var.ssh_pub)}"
  }
  provisioner "remote-exec" {
    inline = [
      "echo SPARK_MASTER_HOST='${google_compute_instance.vm_instance_master[0].network_interface.0.network_ip}' >> /home/am72ghiassi/bd/spark/conf/spark-env.sh",
      "echo SHAPE_VM_SLAVES='${var.machine_type}' >> /tmp/shape_vm_slaves.txt",
      "echo export JAVA_HOME='${var.jdk_version}' >> /home/eginez/.bashrc",
      "source /home/eginez/.bashrc"
      "/home/am72ghiassi/bd/spark/sbin/start-master.sh"
    ]
  }
  
  connection {
    type        = "ssh"
    user        = "${var.user}"
    host        = "${google_compute_instance.vm_instance_master[0].network_interface.0.access_config.0.nat_ip}"
    private_key = "${file(var.ssh_priv)}"
  }
}

resource "google_compute_instance" "vm_instance_slaves" {
  name         = "slaveinstance-${count.index + 1}"
  machine_type = "${var.machine_type}"
  count        = "${var.num_nodes}"
  allow_stopping_for_update = true

  boot_disk {
    initialize_params {
      image = "${data.google_compute_image.bigdl_custom_image.self_link}"
    }
  }

  network_interface {
    # A default network is created for all GCP projects
    network = "default"
    access_config {
    }
  }

  metadata = {
    ssh-keys = "${var.user}:${file(var.ssh_pub)}"
  }

  provisioner "remote-exec" {
    inline = [
      "echo SPARK_MASTER_HOST='${google_compute_instance.vm_instance_master[0].network_interface.0.network_ip}' >> /home/am72ghiassi/bd/spark/conf/spark-env.sh",
      "echo SHAPE_VM_SLAVES='${var.machine_type}' >> /tmp/shape_vm_slaves.txt",
      "echo export JAVA_HOME='${var.jdk_version}' >> /home/eginez/.bashrc",
      "source /home/eginez/.bashrc"
      "/home/am72ghiassi/bd/spark/sbin/start-slave.sh spark://${google_compute_instance.vm_instance_master[0].network_interface.0.network_ip}:7077"
    ]
  }
  
  connection {
    type        = "ssh"
    user        = "${var.user}"
    host = "${self.network_interface.0.network_ip}"
    private_key = "${file(var.ssh_priv)}"
  }

  depends_on = [
       google_compute_instance.vm_instance_master
  ]
}

output "ip_master" {
 value = google_compute_instance.vm_instance_master[0].network_interface.0.access_config.0.nat_ip
}

output "ip_slaves" {
 value = google_compute_instance.vm_instance_slaves.*.network_interface.0.access_config.0.nat_ip
}
