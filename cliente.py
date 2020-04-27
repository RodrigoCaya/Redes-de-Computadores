import socket as sock

direccionServidor = 'localhost'
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
