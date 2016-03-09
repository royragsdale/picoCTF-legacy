#!/bin/bash

python3.4 -b -m pytest --showlocals --junitxml /vagrant/shellresults.xml -s -v ./tests
