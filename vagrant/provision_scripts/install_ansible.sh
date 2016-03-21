#!/bin/bash

# Minimal script to install ansible via pip as described:
# http://docs.ansible.com/ansible/intro_installation.html#latest-releases-via-pip

# Include the following Ansible dependencies
# sshpass for password based ssh
# python-passlib for htpasswd module

# This will get the base boxes to a place where we can use the Vagrant Ansible Local
# Provisioner: https://www.vagrantup.com/docs/provisioning/ansible_local.html

# We are currently stuck at 1.9.2 based on a lack of integration for ansible 2.0
# solution adapted from: https://github.com/mitchellh/vagrant/issues/6793

sudo apt-get update 
sudo apt-get install -y python-pip build-essential python-dev python-passlib sshpass
sudo pip install ansible==1.9.2
sudo cp /usr/local/bin/ansible /usr/bin/ansible
