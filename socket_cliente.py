import socket
import time
import csv
import sys
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

#funcion que crea la ventana de advertencia
#entradas: Valor de temperatura registrado ,Valor de temperatura ideal
#salidas N/A, se levanta una ventana de advertencia
class ventana:
    def levantar_ventana(temp_c,temp_base):

        mensaje_alerta= "La temperatura del aceite esta fuera de lo aceptable. Diferencia de temperatura : " + str(diferencia)+" grados Celsius. Temperatura requerida: " +str(temp_base)+" grados Celsius. Esta es la alarma # "+str(contador_alarmas)+" en este ciclo de trabajo."


        tk.Tk().withdraw() # to avoid showing the root window
        messagebox.showerror(
                title="Alerta de temperatura!",
                message=mensaje_alerta)



#funcion que inciizlia los excel cada vez que se corre el programa
#Entradas: Nombre de las columnas del excel temporal, nombre de las columnas del excel de base de datos
#salidas: Plantillas de excel para cada archivo
def crear_excel(columnas_temp,columnas_machote):
        # Se crea un archivo CSV donde depositar los datos recibidos TEMPORALES
    with open('temp.csv', 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=columnas_temp)
        csv_writer.writeheader()



    # Se crea un archivo CSV para guardar las cosas en formato de la base de datos
    with open('Machote_trazabilidad.csv', 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=columnas_machote)
        csv_writer.writeheader()

# Inicialización del socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP_ADDRS = '192.168.1.211'
s.connect((IP_ADDRS, 5000))

# Declaración de variables iniciales
datos_recibidos = ""
buffer = ""

#esta varaible se us apara medir el tiempo entre las subidas al excel de la base de datos
hora_ultimo_dato= datetime.now()

#Nombres de las columnas del excel temporal
columnas_temp = ["ID","hora_recibido","hora_envio","hora_envio_grafico", "tiempo_procesamiento","freq","temp_c","tiempo_residencia_calculado"]

#nombres de las columnas ajustadas al formato del machote de trazabilidad
columnas_machote=["Hora de la medida","Frecuecnia de la malla del freidor","Temperatura del Aceite","Tiempo de residencia"]

#crea excele inciales
crear_excel(columnas_temp,columnas_machote)

#toma la informacion de la temperatura ideal de aceite
temp_base = int(input(" Por Favor, introduzca la temperatura nominal del aceite: \n"))

#frecuencia de subida a base de datos, en minutos
frecuencia_de_subida=1


contador_medidas=0
# Bucle principal
while True:


    c = datetime.now()
    hora_actual = c.strftime('%H:%M:%S.%f')


    # Recibe paquete de datos del cliente
    buffer += s.recv(1024).decode("utf-8")

    tamano_mensaje=sys.getsizeof(buffer)
    #print(tamano_mensaje)
    
    # El mensaje tiene caracteres /n para dividir cada dato de la frecuencia, por lo que se 
    # usa la función split para separar cada dato de la frecuencia
    if '\n' in buffer:
        lines = buffer.split('\n')
        # Toma el dato más reciente, que es el penúltimo de la lista
        # ya que el último tiende a ser un string vacío
        if len(lines) > 1:
            #estos datos consisten del string de la forma:
            # hora_captura, freq, temp_c
            datos_recibidos = lines[-2]
        #resetea el buffer    
        buffer = lines[-1]


    #se separan datos en lista de sus diferentes variables
    datos_leidos= list(datos_recibidos.split(","))

    #se asigna cada elemento de la lista a sus repectivos valores que miden
    tiempo_procesado=datos_leidos[0]
    hora_envio=datos_leidos[1]
    freq=datos_leidos[2]
    temp_c=datos_leidos[3]
    print(datos_leidos)

    #con estas varaibles, se mide cada cuanto se debe subir a la info al excel
    #de base de datos
    contador_tiempo = c - hora_ultimo_dato
    diferencia_minutos = (contador_tiempo.total_seconds())/60
   



    #varaibles derivads de los valores medidos
    #desviacion de la temperatura ideal
    diferencia_temp= float(temp_c)- temp_base

    #tiempo de residencia, utiliza ecuacion 4.7
    tiempo_residencia= 2.793*float(freq)

    #se recorta el tiempo de envio para que contenga hora, minutos, y decenas de segundos
    envio_con_segundos=hora_envio[:7]


    #si la temperatura excede los limites de 5 grados de la temperatura ideal, se levanta una ventana
    #de advertencia
    if diferencia_temp >= 5 or diferencia_temp <= -5:
        ventana.levantar_ventana(temp_c,temp_base)


    #se actualiza el excel temporal
    with open('temp.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=columnas_temp)

        info_temp = {
            "ID":contador_medidas,
            "hora_recibido": hora_actual,
            "hora_envio": hora_envio,
            "hora_envio_grafico":envio_con_segundos,
            "tiempo_procesamiento":tiempo_procesado,
            "freq": freq,
            "temp_c": temp_c,
            "tiempo_residencia_calculado": tiempo_residencia
        }

        csv_writer.writerow(info_temp)


    #se sube la informacion al excel de la base de datos cada vez que pasa una cantida de minutos
    #igual a "frecuencia de subida"
    if diferencia_minutos >= frecuencia_de_subida: 

        hora_ultimo_dato= datetime.now()
        with open('Machote_trazabilidad.csv', 'a') as csv_file_machote:
            csv_writer = csv.DictWriter(csv_file_machote, fieldnames=columnas_machote)
            info_base_datos = {
                "Hora de la medida": hora_envio,
                "Frecuecnia de la malla del freidor": freq,
                "Temperatura del Aceite": temp_c,
                "Tiempo de residencia": tiempo_residencia,
            }
            csv_writer.writerow(info_base_datos)

    contador_medidas+=1
    print(contador_medidas)
    time.sleep(2)
