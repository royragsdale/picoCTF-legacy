#!/bin/bash

#Default to 3 instances.
INSTANCES=${1:-3}

sudo shell_manager clean

sudo apt-get install -y --force-yes cyberstakes-online-2014
sudo apt-get clean

sudo shell_manager deploy -b cyberstakes-online-2014 -n $INSTANCES
