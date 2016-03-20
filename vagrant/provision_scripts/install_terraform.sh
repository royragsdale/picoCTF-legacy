#!/bin/sh

# Minimal script to install Terraform as described:
# https://www.terraform.io/intro/getting-started/install.html

# This will get the jump box to where it can deploy infrastrucutre to AWS

TERRAFORM_URL=https://releases.hashicorp.com/terraform/0.6.13/terraform_0.6.13_linux_amd64.zip
TERRAFORM_ZIP=terraform_0.6.13_linux_amd64.zip

sudo apt-get install -y unzip
sudo mkdir -p /usr/local/terraform

if [ ! -f /usr/local/terraform/terraform ]
then
    wget -nv $TERRAFORM_URL
    sudo unzip $TERRAFORM_ZIP -d /usr/local/terraform
fi

# [TODO] puts as root
echo "#Add Terraform to path" >> $HOME/.profile
echo "PATH=$PATH:/usr/local/terraform" >> $HOME/.profile
