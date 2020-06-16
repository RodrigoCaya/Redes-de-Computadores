import socket as sock

PuertoTCP = 51556
PuertoUDP = 56988

#Crea el archivo cache.txt si no existe, si no, lee su contenido y lo entrega como lista de tupla
#Esta lista de tupla contiene los valores (link,header)
def cache():
    lista = []
    try:
        cache = open("cache.txt", "r+")
    except(FileNotFoundError):
        cache = open("cache.txt", "w+")
    texto = cache.read()
    splits = texto.split("link",-1)
    temp = (int((len(splits)-1)/2))
    print(temp)
    for i in range(temp+1):
        if(i != 0):
            lista.append((splits[(i*2)-1],splits[2*i]))
    return lista

    
#Agrega el link y header al cache
def agregarCache(lista):
    caxe = open("cache.txt", "w+")
    for link,header in lista:
        caxe.write("link "+link+ "\n")
        caxe.write("link "+header)


#Trabaja el cache en la lista 
#Se visualiza la lista como a-b-c-d-e en los comentarios
def actualizarCache(lista, url):
    retorno = ""
    #Elimina un elemento en la lista y mueve la lista hacia adelante al momento de encontrarlo
    #Ejemplo busca b  a-b-c-d-e -> a-c-d-e-e
    for i in range(len(lista)):
        if(retorno!=""):
            lista[i-1] = lista[i]
        urll,_ = lista[i]
        if(url in urll):
            url_temp = url
            _,retorno = lista[i]
    #Si no encuentra el valor dentro del cache, elimina el primero
    #Ejemplo a-b-c-d-e -> b-c-d-e-e
    if(retorno == ""):                             
        if(len(lista)==5):
            for i in (range(len(lista)-1)): 
                lista[i] = lista[i+1]
    #Si lo encuentra, agrega el encontrado al final
    #Ejemplo a-c-d-e-e -> a-c-d-e-b
    else:                                              
        lista[len(lista)-1] = (url_temp,retorno) 
    return (lista,retorno)


#Elimina el HTML dentro del mensaje, solo deja el header
def cortar(mensaje):
    splits = mensaje.split("<!",1)
    return ((splits[0],splits[0].split()[1]))

#Se conecta con la pagina para realizar un GET
def conectar(mensaje):
    socketServidor = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    socketServidor.connect((mensaje, 80))
    socketServidor.sendall(b"GET / HTTP/1.1\r\nHost: " + mensaje.encode() +b"\r\nAccept: text/html\r\n\r\n")
    mensaje = str(socketServidor.recv(1024), 'utf-8')
    return (cortar(mensaje))
    

#Realiza una conexion UDP con el cliente para entregar el header
def ServidorUDP(header):
    #inet = ipv4 | dgram = udp
    socketServidor = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
    socketServidor.bind(('', PuertoUDP))
    print("Servidor escuchando en puerto:", PuertoUDP)
    while True:
        #Recibe el mensaje del cliente
        mensaje, direccionCliente = socketServidor.recvfrom(2048)
        decodificado = mensaje.decode()
        print("Se recibio: ", decodificado)
        if(decodificado == "OK"):
            #Envia el header al cliente
            socketServidor.sendto(header.encode(),direccionCliente)
        socketServidor.close()
        break
        
#Realiza la conexion TCP con el cliente
def ServidorTCP():
    #inet = ipv4 | stream = TCP
    lista = cache()
    socketServidor = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    socketServidor.bind(('', PuertoTCP))
    #indica que espere el handshake
    socketServidor.listen(1)
    print("Servidor TCP escuchando en puerto: ", PuertoTCP)
    while True:
        socketCliente, _ = socketServidor.accept()
        #Recibe el mensaje del cliente
        mensaje = socketCliente.recv(2048).decode()
        #Termina la conexion TCP
        if(mensaje == "terminate"):
            agregarCache(lista)
            socketServidor.close()
            break
        print("Se recibio: ", mensaje)
        #Se busca en el cache
        lista,estado = actualizarCache(lista,mensaje)
        #Si no se encuentra en el cache
        if(estado == ""):
            header,codigo = conectar(mensaje)
            if(len(lista) < 5):
                lista.append((mensaje,header))                
            else:
                lista[4] = (mensaje,header)
        #Si se encuentra en el cache
        else:
            header = estado
            codigo = "200"
        #Si el header no tiene error
        if(codigo == "200" or codigo == "301"):
            respuesta = str(PuertoUDP)
            #Se envia el puerto UDP
            socketCliente.send(respuesta.encode())
            socketCliente.close()
            #Realiza la conexion UDP
            ServidorUDP(header)
        #Si el header tiene error
        else:
            respuesta = "Error "+codigo
            #Envia el error al cliente
            socketCliente.send(respuesta.encode())
            socketCliente.close()
            
        
ServidorTCP()
