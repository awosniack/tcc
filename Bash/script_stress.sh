#!/bin/bash 

FULL_PATH=/home/pi/radiation-benchmarks/src/openmp/gemm

DELAY=6 #Quantos segundos de MAX_PERFORMANCE em cada execucao

sleep 30

#------------------------------------------------------------------------------>
#COMECAR EXECUCAO DO ARQUIVO DE STRESS AQUI
${FULL_PATH}/gemm_float_check 4 2048 16 ${FULL_PATH}/ma_2048 ${FULL_PATH}/mb_20>
while true
do

    #SET PERFORMANCE HIGH
    eval "sudo cpufreq-set -g performance"

    #esperar pelo tempo delay em max_performance
    sleep $DELAY

    #SET PERFORMANCE LOW
    eval "sudo cpufreq-set -g powersave"

    #esperar pelo tempo delay em min_performance
    sleep $DELAY

done
