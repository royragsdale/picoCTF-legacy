#!/bin/bash

#Dependencies
apt-get install dpkg dpkg-dev fakeroot python3 python3-pip

#Build wheel package
python2 setup.py bdist_wheel
wheel=$(find . | grep "\.whl$")

pip2 install --upgrade $wheel
