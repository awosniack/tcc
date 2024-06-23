#!/bin/bash 

FULL_PATH=/home/pi/radiation-benchmarks/src/openmp/gemm

MAX_CLOCK=2500 #Clock maximo permitido INCLUSIVO
MIN_CLOCK=1750 #Clock minimo permitido (Rasp4 é 600)
INCREMENTO_CLOCK=50 #Passo entre cada incremento de clock

MAX_TENSAO=8 #Tensao maxima permitida (Rasp4 é 8) INCLUSIVO
MIN_TENSAO=0 #Tensao minima permitida (Rasp4 é -16)

ACABOU=-10 #Flag que seta a TENSAO para indicar que acabou

DELAY=7 #Quantos segundos de MAX_PERFORMANCE em cada execucao

COUNT_MIN=1 #Valor inicial da contagem de execucoes
COUNT_MAX=100 #Quantas execucoes para cada tensao e clock

FILE_TENSAO="${FULL_PATH}/tensao.txt" #Arquivo contendo a ultima tensao
FILE_CLOCK="${FULL_PATH}/clock.txt" #Arquivo contendo o ultimo clock
LOGGER_FILE="${FULL_PATH}/log.txt" #Arquivo de log
OUT_FOLDER="${FULL_PATH}/output" #Pasta contendo os arquivos inicio e fim de execucao

TENSAO=$MIN_TENSAO
CLOCK=$MIN_CLOCK

#retorna hh:mm::ss atuais
now() {
   date +"%T"
}

#grava o primeiro parametro no arquivo de log com a data atual
log() {
    echo "$(now) $1" >> $LOGGER_FILE
}
sleep 20
if test "$1" = "clean"; then
    rm -rf $OUT_FOLDER
    rm $FILE_TENSAO
    rm $FILE_CLOCK
    rm $LOGGER_FILE
fi

if [ ! -f "$LOGGER_FILE" ]; then
    touch $LOGGER_FILE
fi

if [ ! -d "$OUT_FOLDER" ]; then
    log "CRIANDO OUTPUT FOLDER"
    mkdir $OUT_FOLDER
fi

if test -f "$FILE_TENSAO"; then
    #arquivo existe
    TENSAO=`tac $FILE_TENSAO |egrep -m 1 .`
    log "TENSAO LIDA FOI DE ${TENSAO}"
    else
    #arquivo nao existe
    log "CRIANDO ARQUIVO TENSAO"
    touch $FILE_TENSAO
    echo "$MIN_TENSAO" > $FILE_TENSAO
fi

#so continuar se a tensao lida for diferente de ACABOU
if test $TENSAO -ne $ACABOU; then

    #lendo ultimo valor do arquivo clock
    if test -f "$FILE_CLOCK"; then
        #arquivo existe
        CLOCK=`tac $FILE_CLOCK |egrep -m 1 .`
    else
        #arquivo nao existe
        log "CRIANDO ARQUIVO CLOCK"
        touch $FILE_CLOCK
        echo "$MIN_CLOCK" > $FILE_CLOCK
    fi


    log "LEITURA INICIAL CONCLUIDA"
    log "TENSAO=${TENSAO} CLOCK=${CLOCK}"
    #Leitura inicial da tensao e clock concluida
    ARQUIVO_COUNT="${OUT_FOLDER}/count_${TENSAO}_${CLOCK}.txt"
    ARQUIVO_OUT="${OUT_FOLDER}/out_${TENSAO}_${CLOCK}.txt"

    #Count marca inicio da execucao
    #Out marca o final de uma execucao bem sucedida
    COUNT=$COUNT_MIN
    OUT=$COUNT_MIN
    #Carregar save do count de execucoes
    if test -f "$ARQUIVO_COUNT"; then
            COUNT=`tac $ARQUIVO_COUNT |egrep -m 1 .`
            ((++COUNT))
        else
            log "CRIANDO ARQUIVO COUNT COM NOME ${ARQUIVO_COUNT}"
            touch $ARQUIVO_COUNT
            echo "$COUNT_MIN" > $ARQUIVO_COUNT
    fi
    if test -f "$ARQUIVO_OUT"; then
            OUT=`tac $ARQUIVO_OUT |egrep -m 1 .`
            ((++OUT))
        else
            log "CRIANDO ARQUIVO OUT COM NOME ${ARQUIVO_OUT}"
            touch $ARQUIVO_OUT
            echo "$COUNT_MIN" > $ARQUIVO_OUT
    fi
    log "Antes do while - tensao=${TENSAO} clock=${CLOCK}"


    #----------------------------------------------------------------------------------------
    #COMECAR EXECUCAO DO ARQUIVO DE STRESS AQUI
    ${FULL_PATH}/gemm_float_check 4 2048 16 ${FULL_PATH}/ma_2048 ${FULL_PATH}/mb_2048 ${FULL_PATH}/gold_2048_m-order_4_ths_16_blocks 1000000 &
    #Enquanto count(numero de execucoes) for menor que o numero maximo de execucoes
    while [ $COUNT -le $COUNT_MAX ]
    do
        #ja escrevo no arquivo que comecou a execucao atual
        log "COMECANDO EXECUCAO ${COUNT}"
        echo "$COUNT" > $ARQUIVO_COUNT
        
        #SET PERFORMANCE HIGH
        eval "sudo cpufreq-set -g performance"

        #esperar pelo tempo delay em max_performance
        sleep $DELAY

        #SET PERFORMANCE MINIMUN
        eval "sudo cpufreq-set -g powersave"

        #escrevendo no arquivo de saida que finalizou a execucao atual
        echo "$OUT" > $ARQUIVO_OUT

        # incrementando as variaveis de contagem de inicio e fim de execucao
        OUT=$((OUT+1))
        COUNT=$((COUNT+1))
    done



    CLOCK=$((CLOCK + ${INCREMENTO_CLOCK}))
    log "CLOCK ATUALIZADO, AGORA É ${CLOCK}"
    #Clock passando do maximo
    if test $CLOCK -gt $MAX_CLOCK; then
        CLOCK=$MIN_CLOCK
        log "CLOCK PASSOU DE ${MAX_CLOCK}, REINICIANDO CLOCK=${CLOCK}"
        ((++TENSAO))
        echo "$TENSAO" > $FILE_TENSAO
        log "TENSAO INCREMENTADA, AGORA TENSAO=${TENSAO}"
    fi

    echo "$CLOCK" > $FILE_CLOCK

    #Tensao passando do maximo
    if test $TENSAO -gt $MAX_TENSAO; then
        log "TENSAO PASSOU DO MAXIMO ------ ACABOU"
        TENSAO=$ACABOU
        echo "$TENSAO" > $FILE_TENSAO
    fi


    log "REINICIAR AGORAAAAAAAAAAAAAAAAAAA"
    sudo sed -i -e "/over_voltage=/ s/=.*/=${TENSAO}/" /boot/config.txt
    sudo sed -i -e "/arm_freq=/ s/=.*/=${CLOCK}/" /boot/config.txt
    
    sudo reboot
    

fi