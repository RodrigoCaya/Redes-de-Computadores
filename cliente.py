import socket as sock
import time

direccionServidor = 'localhost'

def enviarTxt(mensaje):
    f = open("URL.txt","w")
    f.write(mensaje)
    f.close()

def ClienteUDP(respuesta):
    puertoServidor = int(respuesta)
    #inet = ipv4 | dgram = udp
    socketCliente = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
    aEnviar = "OK"
    socketCliente.sendto(aEnviar.encode(), (direccionServidor, puertoServidor))
    #esperar una respuesta
    mensaje, _ = socketCliente.recvfrom(2048)
    #print(mensaje.decode())
    socketCliente.close()
    enviarTxt(mensaje.decode())



def ClienteTCP():
    puertoServidor = 51556
    socketCliente = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    #esta funcion realiza el handshake
    socketCliente.connect((direccionServidor, puertoServidor))
    aEnviar = input('Ingrese texto: ')
    socketCliente.send(aEnviar.encode())
    respuesta = socketCliente.recv(2048).decode()
    socketCliente.close()
    if("Error" in respuesta):
        print(respuesta)
    else:
        time.sleep(1)
        ClienteUDP(respuesta)


#ClienteUDP()
ClienteTCP()