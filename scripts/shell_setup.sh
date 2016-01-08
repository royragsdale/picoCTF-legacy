#!/bin/bash

USER_HOME="/home/vagrant"
ROOT="/vagrant/picoCTF-shell-manager"

# add universe
sudo add-apt-repository "deb http://archive.ubuntu.com/ubuntu $(lsb_release -sc) universe"

apt-get -y update
apt-get -y upgrade

apt-get -y install software-properties-common monit

cd $ROOT

# START of what was previously in picoCTF-shell-manager-install.sh

mkdir /tmp/hacksports/

#if config.py exists, back it up
if [ -f /opt/hacksports/config.py ]; then
    cp /opt/hacksports/config.py /tmp/hacksports/config.py
fi

# Install Dependencies
apt-get install -y dpkg dpkg-dev fakeroot python3 python3-pip socat nginx php5-cli gcc-multilib shellinabox

# Install uwsgi and plugins for shell server
apt-get install -y uwsgi uwsgi-plugin-php uwsgi-plugin-python3 uwsgi-plugin-python python-flask

dpkg -i /vagrant/configs/shellinabox/shellinabox_2.18_amd64.deb

pip3 install --upgrade pip
apt-get remove -y --force-yes python3-pip

# install shell_manager pip package from source
./install.sh

# restore config.py if backed up
if [ -f /tmp/hacksports/config.py ]; then
    cp /tmp/hacksports/config.py /opt/hacksports/config.py
fi

# disable apache if it's running
systemctl disable apache2

# remove default config and restart nginx
rm /etc/nginx/sites-enabled/default
sudo service nginx restart

cp /vagrant/scripts/shellinaboxd.service /lib/systemd/system/
systemctl enable shellinaboxd.service
systemctl start shellinaboxd.service

# PAM module setup
cp $ROOT/config/common-auth /etc/pam.d/common-auth
cp $ROOT/config/sshd_config /etc/ssh/sshd_config

# The python pam module is copied by pip,
# so we just need to install the dependencies here
apt-get install -y libpam-python python-setuptools
sudo service sshd restart

curl https://bootstrap.pypa.io/get-pip.py | python2
pip2 install requests
groupadd competitors


# Securing the shell server
# limits
cp /vagrant/configs/security/limits.conf /etc/security/limits.conf

cp /vagrant/configs/security/sysctl.conf /etc/sysctl.conf
sysctl -p

cp /vagrant/configs/security/isolate-users.service /lib/systemd/system
systemctl enable isolate-users.service
systemctl start isolate-users.service

# set hostname
hostname shell
echo "shell" > /etc/hostname
echo -e "127.0.0.1\tshell" >> /etc/hosts

# make shell_manager.target services run on reboot
sudo systemctl add-wants default.target shell_manager.target

# END of what was previously in picoCTF-shell-manager-install.sh

# modify config.py
shell_manager status
DEPLOY_SECRET="@@@ChAnGeMe!@@@"
echo -e "\nHOSTNAME = '192.168.2.3'\n" >> /opt/hacksports/config.py
echo -e "\nWEB_SERVER = 'http://192.168.2.2'\n" >> /opt/hacksports/config.py
echo -e "\nDEPLOY_SECRET = '$DEPLOY_SECRET'\n" >> /opt/hacksports/config.py

echo "Done"

echo "Setting permissions."
chmod -R 1710 /var/cache/apt
chmod 1710 /etc/apt/sources.list

# Deploy journald config and restart
cp /vagrant/configs/journald/journald.conf /etc/systemd
systemctl restart systemd-journald
journalctl --verify

# Configure and launch monit
cp /vagrant/configs/monit/public-secrets.conf /etc/monit/conf.d

cp /vagrant/configs/monit/base.conf /etc/monit/conf.d
cp /vagrant/configs/monit/shell.conf /etc/monit/conf.d
systemctl enable monit
systemctl start monit
monit reload

# Install the example problems.
EXAMPLE_PROBLEMS_ROOT="/vagrant/picoCTF-problems/Examples"

mkdir -p $USER_HOME/debs $USER_HOME/bundles

shell_manager package -s $USER_HOME -o $USER_HOME/debs $EXAMPLE_PROBLEMS_ROOT
for f in $USER_HOME/debs/*
do
    echo "Installing $f..."
    dpkg -i $f
    apt-get install -fy
done


shell_manager bundle -s $USER_HOME -o $USER_HOME/bundles $EXAMPLE_PROBLEMS_ROOT/Bundles/challenge-sampler.json
shell_manager bundle -s $USER_HOME -o $USER_HOME/bundles $EXAMPLE_PROBLEMS_ROOT/Bundles/challenge-sampler-tools.json

for f in $USER_HOME/bundles/*
do
    echo "Installing bundle: $f..."
    dpkg -i $f
    apt-get install -fy
done

# Fix dependencies
shell_manager deploy -b challenge-sampler
