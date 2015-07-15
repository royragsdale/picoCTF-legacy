#!/bin/bash

#Dependencies
apt-get install -y dpkg dpkg-dev fakeroot python3 python3-pip socat nginx php5-cli gcc-multilib

pip3 install --upgrade pip

apt-get remove -y --force-yes python3-pip

bash -c 'pip3 install --upgrade .'

# PAM module setup
apt-get install -y libpam-python python-setuptools
easy_install pip
pip2 install requests

CONTENT=$(cat /etc/pam.d/common-auth)
echo -e "auth [success=done auth_err=die try_again=reset default=ignore] pam_python.so pam_auth.py\n$CONTENT" > /etc/pam.d/common-auth
echo -e "\nChallengeResponseAuthentication yes\n" >> /etc/ssh/sshd_config
sudo service sshd restart

groupadd competitors
