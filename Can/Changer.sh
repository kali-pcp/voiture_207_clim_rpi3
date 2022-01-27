#!/bin/bash


while read p; do
  echo "$p"
  echo $(echo ${test} | cut -d' ' -f3) ### sort 1D0#22000000000909
done <peptides.txt