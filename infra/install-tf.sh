#!/bin/bash

sudo apt-get install jq unzip git
ssh-keygen
git clone https://github.com/GoogleCloudPlatform/terraform-google-examples.git
cd terraform-google-examples
sh terraform-install.sh

echo Run terraform init to finish

