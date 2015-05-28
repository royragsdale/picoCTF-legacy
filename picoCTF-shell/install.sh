#!/bin/bash

#Dependencies
apt-get install dpkg dpkg-dev fakeroot python3 python3-pip

#Build wheel package
python3 setup.py bdist_wheel
wheel=$(find . | grep "\.whl$")

pip3 install --upgrade $wheel
