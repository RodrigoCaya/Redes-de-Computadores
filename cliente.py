import socket as sock

direccionServidor = 'localhost'

def ClienteUDP():
    # 49152 - 65535
    puertoServidor = 55555
    #inet = ipv4 | dgram = udp
    socketCliente = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
    aEnviar = input("Ingresar texto: ")
    socketCliente.sendto(aEnviar.encode(), (direccionServidor, puertoServidor))
    #esperar una respuesta
    mensaje, _ = socketCliente.recvfrom(2048)
    print(mensaje.decode())
    socketCliente.close()


def ClienteTCP():
    puertoServidor = 55556
    socketCliente = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    #esta funcion realiza el handshake
    socketCliente.connect((direccionServidor, puertoServidor))
    aEnviar = input('Ingrese texto: ')
    socketCliente.send(aEnviar.encode())
    respuesta = socketCliente.recv(2048).decode()
    print(respuesta)
    socketCliente.close()


#ClienteUDP()
#ClienteTCP()