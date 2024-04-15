class Rasp():
    def __init__(self, id, ip, msgOn, msgOff, ackOn, ackOff, ackTimeout, mensagem, mensagemAck, enviado, mensagemLock, tentativas):
        self.id = id
        self.ip = ip
        self.msgOn = msgOn
        self.msgOff = msgOff
        self.ackOn = ackOn
        self.ackOff = ackOff
        self.ackTimeout = ackTimeout
        self.mensagem = mensagem
        self.mensagemAck = mensagemAck
        self.enviado = enviado
        self.mensagemLock = mensagemLock
        self.tentativas = tentativas
