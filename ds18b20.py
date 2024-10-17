import os

#funcion que encuentra el ID del sensor ds18b20 conectado a la Raspberry pi:
#entradas: directorio de control del pin
#salidas: id de conecxion del sensor 
def sensor():
    for i in os.listdir('/sys/bus/w1/devices'):
        if i != 'w1_bus_master1':
            ds18b20 = i
    return ds18b20


#funcion que lee la senal de temepratura del sensor ds18b20
#entradas: id y directorio en el cual se encuentra conectado el sensor
#salidas: lista que contiene la medida en celsius y en farenheit del sensor
def read(ds18b20):

    #se define ufibacion del sensor con us ID
    location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'

    # se abre la ubiacion y se lee
    tfile = open(location)
    text = tfile.read()
    tfile.close()

    #se separa la medida para obtener el dato mas reciente
    secondline = text.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    temperature = float(temperaturedata[2:])

    #mappeo y ajuste de la medida
    celsius = temperature / 1000
    farenheit = (celsius * 1.8) + 32
    return celsius, farenheit
