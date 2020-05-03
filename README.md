2020-1
Rodrigo Cayazaya 201773538-4
Jean-Franco Zárate 201773524-4

Los requerimientos de esta tarea se encuentran en Tarea_1.pdf. Se utilizó el lenguaje Python para su realizacion.

Requisitos:
	- Python 3.8

Esta tarea contiene de dos archivos, "cliente.py" y "servidor.py".

En las lineas 3 y 4 de "servidor.py" se encuentran los valores de puerto para TCP y UDP, respectivamente. 
En las lineas 4 y 25 de "cliente.py" se encuentran el valor de direccion IP del servidor y el puerto del servidor, respectivamente.

Para su correcta ejecucion se debe ejecutar primero "servidor.py" y luego "cliente.py", dentro de este ultimo hay que ingresar una pagina web para obtener su header, el cual se entrega como un archivo ".txt".
El archivo "cliente.py" se puede ejecutar cuantas veces se desee hasta que se introduzca "terminate", el cual termina la conexion TCP.
Al terminar la conexion se creara un archivo "cache.txt", el cual se utiliza como respaldo del cache que utiliza el servidor.