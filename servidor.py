import socket as sock

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