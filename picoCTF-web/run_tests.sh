#!/bin/bash

test_path="./tests"
output_results_prefix="unit"

if [[ -n "$1" ]]; then
  test_path=$1
fi

if [[ -n "$2" ]]; then
  output_results_prefix=$2
fi

python3.4 -b -m pytest --showlocals --junitxml /vagrant/${output_results_prefix}results.xml -s -v "$test_path"
