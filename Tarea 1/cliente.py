import socket as sock
import time

direccionServidor = 'localhost'

#Crea el archivo "url".txt y escribe el header
def enviarTxt(mensaje,link):
    f = open(link+".txt","w")
    f.write(mensaje)
    f.close()

#Realiza la conexion UDP con el servidor
def ClienteUDP(respuesta,link):
    puertoServidor = int(respuesta)
    #inet = ipv4 | dgram = udp
    socketCliente = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
    aEnviar = "OK"
    socketCliente.sendto(aEnviar.encode(), (direccionServidor, puertoServidor))
    mensaje, _ = socketCliente.recvfrom(2048)
    socketCliente.close()
    enviarTxt(mensaje.decode(),link)

#Realiza la conexion TCP con el servidor
def ClienteTCP():
    puertoServidor = 51556
    socketCliente = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    #esta funcion realiza el handshake
    socketCliente.connect((direccionServidor, puertoServidor))
    #Pide la pagina web al usuario
    aEnviar = input('Ingrese pagina web: ')
    #Se envia la pagina web al servidor
    socketCliente.send(aEnviar.encode())
    #Recibe la respuesta del servidor
    respuesta = socketCliente.recv(2048).decode()
    socketCliente.close()
    #Revisa si la respuesta no es un error o si se termino la conexion
    if("Error" in respuesta):
        print(respuesta)
    if(respuesta == ''):
        print("Conexion terminada")
    else:
        time.sleep(1)
        ClienteUDP(respuesta,aEnviar)

ClienteTCP()