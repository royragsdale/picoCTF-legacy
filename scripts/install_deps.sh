#!/bin/bash

# Updates and package installation

sudo apt-get -y update 
sudo apt-get -y upgrade
sudo apt-get -y install unzip
sudo apt-get -y install nginx
sudo apt-get -y install memcached
sudo apt-get -y install libmemcached-dev
sudo apt-get -y install mongodb
sudo apt-get -y install python-setuptools python-dev build-essential
sudo apt-get -y install gunicorn
sudo apt-get -y install git
sudo apt-get -y install exiv2
sudo apt-get -y install python-imaging

sudo easy_install pip
sudo pip install --upgrade virtualenv
sudo pip install Flask
sudo pip install watchdog -U
sudo pip install argcomplete
sudo pip install flask-pymongo
sudo pip install py-bcrypt
sudo pip install pylibmc

# Start nginx

sudo mkdir --parents /srv/http/main-site

sudo service nginx start

