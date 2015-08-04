#!/bin/bash

test_path="./tests"

if [[ -n "$1" ]]; then
  test_path=$1
fi

python3.4 -b -m pytest --showlocals --junitxml results.xml -s -v "$test_path"
