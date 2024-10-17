import time
import socket
import ds18b20
import csv
from datetime import datetime
from read_encoder_v2 import Encoder


#funcion que llama a los modulos de cada sensor:
#salidas: Medida instantanea de cada sensor, hora, minuto, y segundo en que se toman las mediciones
def capturar_datos():
    global encoder, client_socket

    #se toma la hora incial para calcular el tiempo de procesado
    hora_captura=datetime.now()

    #captura de datos de encoder
    periodo = encoder.get_average_period()
    sensor_id = ds18b20.sensor()
    
    #captura de datos del sensor de temperatura
    if ds18b20.read(sensor_id) != None:
        temp_c=ds18b20.read(sensor_id)[0]
    else:
       temp_c=0

    #solo se envia el peridod si esta es mayor a 0
    if periodo != 0:
        freq = 1 / periodo
        freq = round(freq,3)
    else:
        freq = 0
       
    hora_envio=datetime.now()
    tiempo_procesado=hora_envio-hora_captura
    hora_envio=hora_envio.strftime('%H:%M:%S.%f')
      
    #se unen todas las medicion en un solo string
    message = str(tiempo_procesado)+','+str(hora_envio)+','+str(freq) +',' +str(temp_c)+'\n'
    
    
    if freq != 0 and temp_c != 0:
        if client_socket:
            client_socket.send(bytes(message, "utf-8"))
    

    #se escribe a un csv para comparar datos enviados a datos recibidos
    with open('rastreo_integridad.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=columnas_enviadas)

        info_rastreo = {
            "hora_envio": hora_envio,
            "tiempo_procesamiento":tiempo_procesado,
            "freq": freq,
            "temp_c": temp_c
        }

        csv_writer.writerow(info_rastreo)
    
    print(message)
    time.sleep(5)


#funcion de inicializacion del socket del servidor
def socket_listener():
    global client_socket, encoder

    #se abre canal de escucha
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #se inicializa clase dle encoder
    encoder = Encoder(pin_a=17, pin_b=27, ppr=224)

    #una vez que se conecta el cliente, se imprime confirmacion
    s.bind(('', 5000))
    s.listen(15)
    print('SERVIDOR ESTA ESCUCHANDO')


    #bucle principal, se muestrean datos cada 5 segundos
    while True:
        client_socket, address = s.accept()
        
        print(f"Se conecto al cliente de direccion::\n{address}")
        while True:
            capturar_datos() 

client_socket = None
encoder = None

#se crea formato para csv para monitorear datos enviados
columnas_enviadas=["hora_envio", "tiempo_procesamiento","freq","temp_c"]
with open('rastreo_integridad.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=columnas_enviadas)
    csv_writer.writeheader()

#llamada a funcion principal
socket_listener()


