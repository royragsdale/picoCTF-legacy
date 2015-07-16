#!/bin/bash

#Dependencies
apt-get install -y dpkg dpkg-dev fakeroot python3 python3-pip socat nginx php5-cli gcc-multilib

pip3 install --upgrade pip

apt-get remove -y --force-yes python3-pip

bash -c 'pip3 install --upgrade .'

# PAM module setup
# The sshd_config and pam common-auth files are
# copied by pip, so we just need to install the
# dependencies here
apt-get install -y libpam-python python-setuptools
easy_install pip
pip2 install requests
groupadd competitors
sudo service sshd restart
