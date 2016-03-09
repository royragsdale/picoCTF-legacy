#!/bin/bash

ROOT="/vagrant/picoCTF-web"

# Updates
apt-get -y update
apt-get -y upgrade

# CTF-Platform Dependencies
apt-get -y install python3-pip nginx mongodb gunicorn git libzmq-dev nodejs-legacy npm
apt-get -y install ruby-dev dos2unix tmux jekyll phantomjs monit firefox xvfb

npm install -g coffee-script react-tools jsxhint coffee-react

cd $ROOT
./install.sh

# Configure Environment
echo "PATH=\$PATH:$ROOT/scripts" >> /etc/profile

# Configure Nginx
rm /etc/nginx/sites-enabled/default
cp $ROOT/config/ctf.nginx /etc/nginx/sites-enabled/ctf
mkdir -p /srv/http/ctf
service nginx restart

cp /vagrant/scripts/ctf.service /lib/systemd/system/
systemctl enable ctf.service
systemctl start ctf.service

api_manager database clear problems,bundles,submissions,users,teams,groups,shell_servers

python3 /vagrant/scripts/load_problems.py
python3 /vagrant/scripts/start_competition.py

# Configure and launch monit

cp /vagrant/configs/monit/public-secrets.conf /etc/monit/conf.d

cp /vagrant/configs/monit/base.conf /etc/monit/conf.d
cp /vagrant/configs/monit/web.conf /etc/monit/conf.d
systemctl enable monit
systemctl start monit
monit reload
