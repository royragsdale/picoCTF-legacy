#!/bin/bash

sudo shell_manager clean

sudo apt-get install -y --force-yes cyberstakes-online-2014

#Default to 3 instances.
sudo shell_manager deploy -b cyberstakes-online-2014 -n 3
