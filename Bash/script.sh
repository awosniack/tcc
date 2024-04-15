#!/bin/bash
IP='10.10.10.10'
input=''
echo "digite 'up' para criar um loopback no endereço de rede $IP"
echo "digite 'down' para excluir o loopback"
echo "digite 'exit' para sair"
while [ "$input" != "exit" ]
do
        read input
        case $input in
            up)
                sudo ifconfig lo:100 $IP netmask 255.255.255.0 up
                echo "Loopback criado no endereco $IP com sucesso"
            ;;
            down)
                sudo ifconfig lo:100 down
                echo "Loopback excluido do endereco $IP com sucesso"
            ;;
            exit)
                sudo ifconfig lo:100 down
            ;;
            *)
                echo "digite 'up' para criar um loopback no endereço de rede $IP"
                echo "digite 'down' para excluir o loopback"
                echo "digite 'exit' para sair"
            ;;
        esac
done