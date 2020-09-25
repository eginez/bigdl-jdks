
## Inputs ssh public key
## GCP project id
## image name
## machine type
## number of nodes

provider "google" {
 # credentials = file("CREDENTIALS_FILE.json")
 #eg: project     =  "personal-279219"
 project     =  ""
 region      = "europe-west4"
 zone      = "europe-west4-a"
}

data "google_compute_image" "bigdl_custom_image" {
  # Change this to your image name
  name = "bigdl-jdks"
}

variable "num_nodes" {
  description = "Number of nodes to create"
  default     = 1
}

variable "machine_type" {
  description  = "They type of machine dictates the number of vcpus in it, see: https://cloud.google.com/compute/docs/machine-types#e2_machine_types_beta"
  default = "e2-highmem-16" #16 vcpus
}

# user name for ssh key
variable "user" {}

#path to the key file
variable "ssh_pub" {}

resource "google_compute_instance" "vm_instance_master" {
  name         = "master-instance"
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
}

output "ip_master" {
 value = google_compute_instance.vm_instance_master[0].network_interface.0.access_config.0.nat_ip
}

output "ip_slaves" {
 value = google_compute_instance.vm_instance_slaves.*.network_interface.0.access_config.0.nat_ip
}
