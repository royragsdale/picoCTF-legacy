#!/bin/bash

# Minimal script to install ansible via pip as described:
# http://docs.ansible.com/ansible/intro_installation.html#latest-releases-via-pip

# Include the following Ansible dependencies
# sshpass for password based ssh
# python-passlib for htpasswd module

# This will get the base boxes to a place where we can use the Vagrant Ansible Local
# Provisioner: https://www.vagrantup.com/docs/provisioning/ansible_local.html


# We need to use version >2 in order to fix non-executable invetory on windows:
# ref: https://github.com/ansible/ansible/issues/10068
# We are currently stuck at 1.9.2 based on a lack of integration for ansible 2.0
# solution adapted from: https://github.com/mitchellh/vagrant/issues/6793

sudo apt-get update 
sudo apt-get install -y python-pip build-essential python-dev python-passlib sshpass
sudo pip install ansible==2.0.2.0
sudo cp /usr/local/bin/ansible /usr/bin/ansible


# In order to use ansible >1.9.2 with vagrant (1.8.1) ansible_local provisioner 
# we also need to patch ansible-galaxy to correctly detect ansible is installed

# Patch for https://github.com/mitchellh/vagrant/issues/6793 from @MasonM
# should be removed once vagrant >1.8.1 is released and ansible_local correctly
# detects ansible being installed.
# patches https://github.com/mitchellh/vagrant/blob/25ff027b08582978981ed28754a3fed21953a90e/plugins/provisioners/ansible/provisioner/guest.rb#L35-L65

GALAXY='/usr/local/bin/ansible-galaxy'
FIX="if sys.argv == ['$GALAXY', '--help']: sys.argv.insert(1, 'info')"

[[ ! -f $GALAXY ]] || grep -F -q "$FIX" $GALAXY || sed -i "/__main__/a \\    $FIX" $GALAXY
