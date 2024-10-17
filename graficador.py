
import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


plt.style.use('fivethirtyeight')

#funcion de animacion, es el bucle principal que refresca el grafico cada vez que se 
#actualiza el temp.csv
def animate(i):

    #se lee el estado actuial de temp.csv
    entrada_datos = pd.read_csv('temp.csv')

    #se toman los valores de cada columna
    lista_tiempo=entrada_datos["hora_envio_grafico"]
    lista_freq=entrada_datos["freq"]
    lista_temp=entrada_datos["temp_c"]

    #se coratn las listas para contener solo los 10 valores mas recientes
    lista_tiempo=lista_tiempo[-10:]
    lista_freq=lista_freq[-10:]
    lista_temp=lista_temp[-10:]

    #se asignaa listas a variables de los ejes
    x = lista_tiempo
    y1 = lista_freq
    y2 = lista_temp

    #se refresca el grafico y se asignan etiquetas a las variables
    plt.cla()

    plt.plot(x, y1, label='Frecuencia (Hz)')
    plt.plot(x, y2, label='Temperatura (Celsius)')

    plt.legend(loc='upper left')
    plt.tight_layout()



#ejecucion de la funcion principal
ani = FuncAnimation(plt.gcf(), animate,interval=1000)

#despliegue dle grafico
plt.tight_layout()
plt.show()
