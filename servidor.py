import socket as sock


def ServidorUDP():
    # 49152 - 65535
    serverPort = 55555
    #inet = ipv4 | dgram = udp
    socketServidor = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
    socketServidor.bind(('', serverPort))
    print("Servidor escuchando en puerto:", serverPort)
    while True:
        mensaje, direccionCliente = socketServidor.recvfrom(2048)#la cantidad de bits que recive a través del socket - tamaño del buffer
        decodificado = mensaje.decode()
        print("Se recibio: ", decodificado)
        respuesta = "Respuesta: " + decodificado.upper()#dejarlo en mayuscula
        socketServidor.sendto(respuesta.encode(),direccionCliente)
        socketServidor.close()

def ServidorTCP():
    serverPort = 55556
    #inet = ipv4 | stream = TCP
    socketServidor = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    socketServidor.bind(('', serverPort))
    #hay qe decirle que empiece a escuchar las conexiones
    #indica que espere el handshake
    socketServidor.listen(1) #el parametro indica la cantidad maxima de cola
    print("Servidor TCP escuchando en puerto: ", serverPort)
    while True:
        socketCliente, direccionCliente = socketServidor.accept()
        mensaje = socketCliente.recv(2048).decode()
        print("Se recibio: ", mensaje)
        respuesta = "Respuesta: "+ mensaje.upper()
        socketCliente.send(respuesta.encode())
        socketCliente.close()

#ServidorUDP()
ServidorTCP()



