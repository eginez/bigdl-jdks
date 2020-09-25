
provider "google" {
 # credentials = file("CREDENTIALS_FILE.json")
 project     =  "personalprojects-279219"
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

resource "google_compute_instance" "vm_instance_master" {
  name         = "master-instance"
  machine_type = "f1-micro"
  count        = "1"

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
}

resource "google_compute_instance" "vm_instance_slaves" {
  name         = "slaveinstance-${count.index + 1}"
  machine_type = "${var.machine_type}"
  count        = "${var.num_nodes}"
  allow_stopping_for_update = true

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-9"
    }
  }

  network_interface {
    # A default network is created for all GCP projects
    network = "default"
    access_config {
    }
  }
}
