import serial
import exitFlag
import threading
import queue
import signal
import myThread
from rasp import Rasp

dispositivos = []

dispositivos.append(Rasp(id=1, ip='192.168.1.32', msgOn='Ligar4',
                    msgOff='Desligar4', ackOn='4ON', ackOff='4OFF', ackTimeout=0, mensagem='', mensagemAck='', enviado=False, mensagemLock=threading.Lock(), tentativas=0))
dispositivos.append(Rasp(id=2, ip='192.168.1.33', msgOn='Ligar8',
                    msgOff='Desligar8', ackOn='8ON', ackOff='8OFF', ackTimeout=0, mensagem='', mensagemAck='', enviado=False, mensagemLock=threading.Lock(), tentativas=0))

ACK_TIMEOUT = 5 # quantos segundos aguardar pelo ack da mensagem antes de reenviar
TIMEOUT = 15  # segundos - timeout em ping
MAXIMO_TENTATIVAS = 6  # tentativas antes de reiniciar o aparelho
TENTATIVAS = 0
serialPort = serial.Serial(port="/dev/ttyUSB0", baudrate=115200, timeout=0.1)

serialLock = threading.Lock()
threadId = 1
threads = []
exitFlag = exitFlag.exitFlag()

# definindo as threads
userInputThreadDef = {'tName': 'userInput',
                      'f': myThread.userInput,
                      'args': {
                          'exitFlag': exitFlag.check,
                          'dispositivos': dispositivos
                      }
                      }
receiveMessageThreadDef = {'tName': 'receiveMessage',
                           'f': myThread.receiveMessage,
                           'args': {
                               'exitFlag': exitFlag.check,
                               'serialLock': serialLock,
                               'serialPort': serialPort,
                               'dispositivos': dispositivos,
                           }
                           }
sendMessageThreadDef = {'tName': 'sendMessage',
                        'f': myThread.sendMessage,
                        'args': {'exitFlag': exitFlag.check,
                                 'serialLock': serialLock,
                                 'serialPort': serialPort,
                                 'dispositivos': dispositivos,
                                 'ackTimeout': ACK_TIMEOUT
                                 }
                        }
pingThreadName = 'ping'
pingThreadDef = {'tName': pingThreadName,
                #  'f': myThread.ping,
                #  'args': {'exitFlag': exitFlag.check,
                #           'dispositivo': [],
                #           'timeout': TIMEOUT,
                #           'tentativas': TENTATIVAS,
                #           'maxTentativas': MAXIMO_TENTATIVAS
                #           }
                 }
threadsToCreate = [
    userInputThreadDef,
    receiveMessageThreadDef,
    sendMessageThreadDef,
    # pingThreadDef
]

# Capturando o control C para encerrar tudo


def signal_handler(sig, frame):
    exitFlag.exit()


signal.signal(signal.SIGINT, signal_handler)

# Criando threads
for t in threadsToCreate:
    if t['tName'] == pingThreadName:
        for dispositivo in dispositivos:
            threadName  = t['tName'] + str(dispositivo.id)
            # print("Criando ping dispositivo:" + str(dispositivo.id))
            pingThreadDef = {   'tName': threadName,
                                'f': myThread.ping,
                                'args': {'exitFlag': exitFlag.check,
                                        'dispositivo': dispositivo,
                                        'timeout': TIMEOUT,
                                        'tentativas': TENTATIVAS,
                                        'maxTentativas': MAXIMO_TENTATIVAS
                                        }
                 }
            thread = myThread.myThread(threadId, pingThreadDef['tName'], pingThreadDef['f'], pingThreadDef['args'])
            thread.start()
            threads.append(thread)
            threadId += 1
    else:
        thread = myThread.myThread(threadId, t['tName'], t['f'], t['args'])
        thread.start()
        threads.append(thread)
        threadId += 1

for t in threads:
    t.join()
print("Exiting main thread")
