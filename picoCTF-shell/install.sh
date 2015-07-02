#!/bin/bash

#Dependencies
apt-get install -y dpkg dpkg-dev fakeroot python3 python3-pip socat nginx php5-cli gcc-multilib

pip3 install --upgrade pip

sudo apt uninstall python3-pip

bash -c 'pip3 install --upgrade .'
