Descripción de los archivos encontrados en este repositorio:

1) controlador_motor_dc.py : archivo utilizado durante las pruebas de validación para controlar la frecuencia de rotación del motor DC conectado al encoder.
2) ds18b20.py: archivo utilizado en las pruebas de validación físicas para controlar el sensor de temperatura auxiliar ds18b20
3) graficador.py: secuencia lógica para desplegar el gráfico en tiempo real de las variables de la máquina.
4) leer_encoder_v2.py : segunda versión del módulo utilizado en el servidor para leer las entradas del encoger e interpretarlas en forma de un periodo y frecuencia de rotación.
5) Simulacion_RTD.ino: secuencia de control para el MAX31865 y el sensor RTD PT100 cargado al microcontrolador simulado en Proteos LAB v8.
6) socket_cliente.py: archivo principal de control del cliente, recibe datos del servidor y aplica el formato necesario para usarlos en la base de datos y el graficador.
7) socket_servidor.py: recolecta mediciones de los módulos ds18b20.py y leer_encoder_v2.py, los compacta en un string, y los envía al cliente.
8) socket_servidor_rastreo.py: idéntico a socket_servidor.py, con la excepción de que crea un archivo .CSV con todos los datos enviados al cliente, utilizado en la prueba de validación: "Prueba general de integridad y velocidad"
