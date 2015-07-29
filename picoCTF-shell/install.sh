#!/bin/bash

# get directory of this script
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

#if config.py exists, back it up
mkdir /tmp/hacksports/
cp /opt/hacksports/config.py /tmp/hacksports/config.py

#Dependencies
apt-get install -y dpkg dpkg-dev fakeroot python3 python3-pip socat nginx php5-cli gcc-multilib shellinabox

pip3 install --upgrade pip
apt-get remove -y --force-yes python3-pip

bash -c 'pip3 install --upgrade --verbose .'

# restore config.py if backed up
cp /tmp/hacksports/config.py /opt/hacksports/config.py

# disable apache if it's running
systemctl disable apache2

# remove default config and restart nginx
rm /etc/nginx/sites-enabled/default
sudo service nginx restart

# add shellinabox to cron
crontab -u root /opt/hacksports/shellinabox/shellinabox_cron

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

# disable ASLR
echo "kernel.randomize_va_space=0" >> /etc/sysctl.conf
sysctl -p

# set hostname
hostname shell
echo "shell" > /etc/hostname
echo -e "127.0.0.1\tshell" > /etc/hosts
