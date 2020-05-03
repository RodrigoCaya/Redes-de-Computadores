import socket as sok


def ServidorTCP():
    socketServidor = sok.socket(sok.AF_INET, sok.SOCK_STREAM)
    socketServidor.connect(("www.aedo.com", 80))
    socketServidor.sendall(b"GET / HTTP/1.1\r\nHost: www.aedo.com\r\nAccept: text/html\r\n\r\n")
    print(str(socketServidor.recv(1024), 'utf-8'))

ServidorTCP()
