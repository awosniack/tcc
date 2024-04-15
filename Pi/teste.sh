#!/bin/bash

cons="sudo cpufreq-set -g conservative"
perf="sudo cpufreq-set -g performance"

while true
do
	sleep 10
	eval "$perf"
	sleep 1
	eval "$cons"
done
