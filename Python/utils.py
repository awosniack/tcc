def newMessage(serialPort):
    return serialPort.in_waiting > 0


def decodeMessage(serialPort):
    message = serialPort.readline()
    try:
        decodedMessage = message.decode("Ascii")
    except:
        return "Erro ao decodificar mensagem"
    return (decodedMessage)


def encodeMessage(serialPort, message):
    try:
        serialPort.write(str.encode(message))
    except:
        return "Erro ao enviar mensagem"
    return (message)


def readUserInput():
    var = str(input())
    print(var)
    return var

