#!/bin/bash

USER_HOME="/home/admin" 

# Install the example problems.
EXAMPLE_PROBLEMS_ROOT="/picoCTF-problems-private/picoCTF-3"

mkdir -p $USER_HOME/debs $USER_HOME/bundles

shell_manager package -s $USER_HOME -o $USER_HOME/debs $EXAMPLE_PROBLEMS_ROOT
for f in $USER_HOME/debs/*
do
    echo "Installing $f..."
    dpkg -i $f
    apt-get install -fy
done


shell_manager bundle -s $USER_HOME -o $USER_HOME/bundles $EXAMPLE_PROBLEMS_ROOT/Bundles/availible-challenges.json
shell_manager bundle -s $USER_HOME -o $USER_HOME/bundles $EXAMPLE_PROBLEMS_ROOT/Bundles/storyline-stubs.json

for f in $USER_HOME/bundles/*
do
    echo "Installing bundle: $f..."
    dpkg -i $f
    apt-get install -fy
done

shell_manager deploy -n 2 -b availible-challenges
shell_manager deploy -n 2 -b storyline-stubs
