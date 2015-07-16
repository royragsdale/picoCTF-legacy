#!/bin/bash

# get directory of this script
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

#Dependencies
apt-get install -y dpkg dpkg-dev fakeroot python3 python3-pip socat nginx php5-cli gcc-multilib

pip3 install --upgrade pip

apt-get remove -y --force-yes python3-pip

bash -c 'pip3 install --upgrade --verbose .'

# PAM module setup
cp $DIR/config/common-auth /etc/pam.d/common-auth
cp $DIR/config/sshd_config /etc/ssh/sshd_config

# The python pam module is copied by pip,
# so we just need to install the dependencies here
apt-get install -y libpam-python python-setuptools
sudo service sshd restart
easy_install pip
pip2 install requests
groupadd competitors
