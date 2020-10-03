#!/bin/bash

sudo apt-get install jq unzip git
ssh-keygen
git clone https://github.com/GoogleCloudPlatform/terraform-google-examples.git
cd terraform-google-examples
bash -x terraform-install.sh

cd ../
git clone https://github.com/eginez/bigdl-jdks.git
cd bigdl-jdks/infra

echo Run terraform init to finish

