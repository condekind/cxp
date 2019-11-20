#!/usr/bin/bash

info_arr=($( find suites/**/* -name "info.sh" ))
echo ${#info_arr[@]}
#for info in ${info_arr[@]}; do
#  # get $info folder, cd to it
#  cfiles=($(find . -name '*.c' -printf '%p\n' | sort -u ))
#done
