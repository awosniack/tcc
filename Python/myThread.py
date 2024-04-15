import threading
import utils
import time
import ping3


# Cria uma thread que recebe um ID, nome, uma funcao para executar e os parametros dessa funcao e os armazena como um dicionario


class myThread (threading.Thread):
    def __init__(self, threadID, name, f, args):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.f = f
        self.args = args

    def run(self):
        print("Starting " + self.name)
        self.f(self.args)
        print("Exiting " + self.name)

# Thread que recebe as mensagens
# (serialPort, serialLock, exitFlag)


def receiveMessage(dic):
    while not dic['exitFlag']():
        dic['serialLock'].acquire()
        if (utils.newMessage(dic['serialPort'])):
            mensagem = utils.decodeMessage(dic['serialPort'])
            mensagem_split = mensagem.split('|')
            for m in mensagem_split:
                if not m == '':
                    print("Mensagem recebida ->" + m)
                    for dispositivo in dic['dispositivos']:
                        if(dispositivo.mensagemAck == m):
                            print("Ack dispositivo " + str(dispositivo.id) + " recebido")
                            dispositivo.mensagemLock.acquire()
                            dispositivo.mensagem = ''
                            dispositivo.mensagemAck = ''
                            dispositivo.mensagemLock.release()
        dic['serialLock'].release()
        time.sleep(1)

# Thread que envia as mensagens de 'messages'
# (serialPort, serialLock, messages, messagesLock, exitFlag)


def sendMessage(dic):
    while not dic['exitFlag']():
        for dispositivo in dic['dispositivos']:
            dispositivo.mensagemLock.acquire()
            if (not dispositivo.mensagem == ''):
                if (dispositivo.ackTimeout > 0):
                    dispositivo.ackTimeout -= 1
                else:
                    dic['serialLock'].acquire()
                    utils.encodeMessage(dic['serialPort'], dispositivo.mensagem)
                    dispositivo.ackTimeout = dic['ackTimeout']
                    print("Dispositivo:" + str(dispositivo.id) + " - sendMessage - " + dispositivo.mensagem)
                    dic['serialLock'].release()
            dispositivo.mensagemLock.release()

        time.sleep(1)

# Thread que le entradas do usuário e coloca em 'messages'
# (exitFlag, messages, messagesLock)


def userInput(dic):
    while not dic['exitFlag']():
        print("exitValue = " + str(dic['exitFlag']()))
        input = utils.readUserInput()
        inputs = input.split()
        if(len(inputs) == 2):
            id = int(inputs[0])
            print("Dispositivo:" + str(id))
            for dispositivo in dic['dispositivos']:
                if(dispositivo.id == id):
                    dispositivo.mensagemLock.acquire()
                    print("Mensagem do dispositivo - " + inputs[1])
                    mensagem = ''
                    mensagemAck = ''
                    if(inputs[1] == dispositivo.msgOn):
                        mensagem = dispositivo.msgOn
                        mensagemAck = dispositivo.ackOn
                    if(inputs[1] == dispositivo.msgOff):
                        mensagem = dispositivo.msgOff
                        mensagemAck = dispositivo.ackOff
                    dispositivo.mensagem = mensagem
                    dispositivo.mensagemAck = mensagemAck
                    dispositivo.ackTimeout = 0
                    dispositivo.mensagemLock.release()


def ping(dic):
    while not dic['exitFlag']():
        dispositivo = dic['dispositivo']
        response = ping3.ping(dispositivo.ip, timeout=dic['timeout'])
        resposta = dispositivo.msgOff if (response == None or response == False) else dispositivo.msgOn

        if resposta == dispositivo.msgOff:
            print("Dispositivo:" + str(dispositivo.id) + " - pingThread - " + dispositivo.msgOff)
            if dispositivo.enviado == True:
                print("Dispositivo:" + str(dispositivo.id) +" - pingThread - " + dispositivo.msgOn)
                dispositivo.mensagemLock.acquire()
                dispositivo.mensagem = dispositivo.msgOn
                dispositivo.mensagemAck = dispositivo.ackOn
                dispositivo.enviado = False
                dispositivo.ackTimeout = 0
                dispositivo.mensagemLock.release()
                dispositivo.tentativas = 0
            else:
                dispositivo.tentativas += 1
            
        else:
            print("Dispositivo:" + str(dispositivo.id) + " - pingThread - " + dispositivo.msgOn)
            time.sleep(dic['timeout'])
            dispositivo.tentativas = 0
            
        if dispositivo.tentativas >= dic['maxTentativas']:
            print("Dispositivo:" + str(dispositivo.id) + " - pingThread - " + dispositivo.msgOff)
            dispositivo.mensagemLock.acquire()
            dispositivo.mensagem = dispositivo.msgOff
            dispositivo.mensagemAck = dispositivo.ackOff
            dispositivo.enviado = True
            dispositivo.ackTimeout = 0
            dispositivo.mensagemLock.release()
