import socket as sock

#0) el TCP servidor tiene que enviar al TCP cliente qe la url esta disponible o no, y tambien enviar el puerto del UDP (55555) LISTOOOO 
#1) cortar el header (hasta el <!DOCTYPE) LISTOOOOOO
#1.5) hacer el quit del udp LISTOOOOO
#2) hacer el cache
#3) Cambiar a UDP LISTOOOOO
#4) enviar el header por UDP LISTOOOO
#5) escribir el header en URL.txt LISTOOOO

#cache
#1) crear cache.txt F1
#2) crear la lista y qe se actualice al iniciar el servidor F1
#3) buscar el header en la lista y retornarlo F2
#3.1) en caso de que esté, retornar F2
#3.2) caso contrario, borrar el primer url, retornar F2
#4) mover los header hacia adelante F2
#5) agregar ese link al final de la lista (link \n header) F2
#6) actualizar cache.txt antes de cerrar el servidor F2


#cache.txt:
#aedo.com
#jean.com
#caya.com
#pantufla.com
#google.com

#| 1 | 2 | 3 | 4 | 5 |


#*) VER CASOS DONDE LA WEA NO FUNCIONA (www.caya.cl)

PuertoTCP = 51556
PuertoUDP = 56988

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

    
    

def agregarCache(lista):
    caxe = open("cache.txt", "w+")
    for link,header in lista:
        caxe.write("link "+link+ "\n")
        caxe.write("link "+header)


     

def actualizarCache(lista, url):
    retorno = ""
    for i in range(len(lista)):   #busca uno por uno en la lista y cuando encuentra pasa a los siguies hacia adelante # a-b-c -> a-c-c
        #print("i = ", i)
        if(retorno!=""):
            lista[i-1] = lista[i]
        urll,_ = lista[i]
        if(url in urll):
            #print("entreeeeee")
            url_temp = url
            _,retorno = lista[i]
        #print("listaaaa = ",lista)
    if(retorno == ""):                             
        if(len(lista)==5):
            for i in (range(len(lista)-1)): # a-b-c-d-e -> b-c-d-e-e
                lista[i] = lista[i+1]
    else:                                              
        lista[len(lista)-1] = (url_temp,retorno) # a-c-c -> a-c-b
    #print("listaaaa : ",lista)
    return (lista,retorno)


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
    

def ServidorUDP(header):
    #inet = ipv4 | dgram = udp
    #print("HOLAAAAAA")
    socketServidor = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
    socketServidor.bind(('', PuertoUDP))
    print("Servidor escuchando en puerto:", PuertoUDP)
    while True:
        mensaje, direccionCliente = socketServidor.recvfrom(2048)#la cantidad de bits que recive a través del socket - tamaño del buffer
        decodificado = mensaje.decode()
        print("Se recibio: ", decodificado)
        if(decodificado == "OK"):
            socketServidor.sendto(header.encode(),direccionCliente)
        socketServidor.close()
        break
        #respuesta = decodificado.upper()#dejarlo en mayuscula
        

def ServidorTCP():
    #inet = ipv4 | stream = TCP
    lista = cache()
    #print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",len(lista))
    socketServidor = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    socketServidor.bind(('', PuertoTCP))
    #hay qe decirle que empiece a escuchar las conexiones
    #indica que espere el handshake
    socketServidor.listen(1) #el parametro indica la cantidad maxima de cola
    print("Servidor TCP escuchando en puerto: ", PuertoTCP)
    while True:
        socketCliente, direccionCliente = socketServidor.accept()
        mensaje = socketCliente.recv(2048).decode()
        if(mensaje == "terminate"):
            agregarCache(lista)
            break
        print("Se recibio: ", mensaje)
        #print("LISTAAAAAAA ",lista)
        lista,estado = actualizarCache(lista,mensaje)
        #print("LISTAAAAAAA ",lista)
        if(estado == ""):
            header,codigo = conectar(mensaje)
            if(len(lista) < 5):
                lista.append((mensaje,header))
                #print("LISTAAAAAAA =  ",lista)
                
            else:
                lista[4] = (mensaje,header)
                #print("LISTAAAAAAA:  ",lista)

        else:
            header = estado
            codigo = "200"
        if(codigo == "200" or codigo == "301"):
            respuesta = str(PuertoUDP)
            socketCliente.send(respuesta.encode())
            socketCliente.close()
            ServidorUDP(header)
            
        else:
            respuesta = "Error "+codigo
            socketCliente.send(respuesta.encode())
            socketCliente.close()
            
        

#ServidorUDP()  
ServidorTCP()

#lista = [("l1","h1"),("l2","h2"),("l3","h3"),("l4","h4"),("l5","h5")]
#print("PRUEBA 1: ",actualizarCache(lista,"l1"))
#print("PRUEBA 2: ",actualizarCache(lista,"l6"))
#print("PRUEBA 3: ",actualizarCache(lista,"l3"))
#print("PRUEBA 0: ",actualizarCache(lista,"l1"))

#cache()
