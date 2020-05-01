import socket as sock

#0) el TCP servidor tiene que enviar al TCP cliente qe la url esta disponible o no, y tambien enviar el puerto del UDP (55555) LISTOOOO 
#1) cortar el header (hasta el <!DOCTYPE) LISTOOOOOO
#1.5) hacer el quit del udp LISTOOOOO
#2) hacer el cache
#3) Cambiar a UDP
#4) enviar el header por UDP
#5) escribir el header en URL.txt

#*) VER CASOS DONDE LA WEA NO FUNCIONA (www.caya.cl)

PuertoTCP = 55556
PuertoUDP = 55555


#funcion para cortar el get para solo tener el header, osea, cortar hasta el DOCTYPE
def cortar(mensaje):
    splits = mensaje.split("<!",1)
    return ((splits[0],splits[0].split()[1]))


def conectar(mensaje):
    socketServidor = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    socketServidor.connect((mensaje, 80))
    socketServidor.sendall(b"GET / HTTP/1.1\r\nHost: " + mensaje.encode() +b"\r\nAccept: text/html\r\n\r\n")
    mensaje = str(socketServidor.recv(1024), 'utf-8')
    return (cortar(mensaje))
    

def ServidorUDP(mensaje):
    #inet = ipv4 | dgram = udp
    socketServidor = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
    socketServidor.bind(('', PuertoUDP))
    print("Servidor escuchando en puerto:", PuertoUDP)
    while True:
        mensaje, direccionCliente = socketServidor.recvfrom(2048)#la cantidad de bits que recive a través del socket - tamaño del buffer
        decodificado = mensaje.decode()
        print("Se recibio: ", decodificado)
        respuesta = decodificado.upper()#dejarlo en mayuscula
        socketServidor.sendto(respuesta.encode(),direccionCliente)
        socketServidor.close()

def ServidorTCP():
    #inet = ipv4 | stream = TCP
    socketServidor = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    socketServidor.bind(('', PuertoTCP))
    #hay qe decirle que empiece a escuchar las conexiones
    #indica que espere el handshake
    socketServidor.listen(1) #el parametro indica la cantidad maxima de cola
    print("Servidor TCP escuchando en puerto: ", PuertoTCP)
    while True:
        socketCliente, direccionCliente = socketServidor.accept()
        mensaje = socketCliente.recv(2048).decode()
        if(mensaje == "quit"):
            break
        print("Se recibio: ", mensaje)
        header,codigo = conectar(mensaje)
        print(codigo)
        print(header)
        #mensaje = mensaje.encode()
        #socketServidor.sendall(b"GET / HTTP/1.1\r\nHost: " + mensaje +b"\r\nAccept: text/html\r\n\r\n")
        if(codigo == "200"):
            respuesta = str(PuertoUDP)
        else:
            respuesta = "Error "+codigo
        socketCliente.send(respuesta.encode())
        socketCliente.close()

#ServidorUDP()  
ServidorTCP()

