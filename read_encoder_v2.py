import RPi.GPIO as GPIO
import time
from collections import deque

#clase creada para incializar encoder
class Encoder:
    #funcion de inicializacion
    #entradas: numeros de pin a los que estan conectadas las senales a y b , ppr del sensor
    def __init__(self, pin_a, pin_b, ppr):
        self.pin_a = pin_a
        self.pin_b = pin_b
        self.ppr = ppr
        self.pulse_count = 0
        self.rotation_end_time = time.time()
        self.rotation_start_time = time.time()
        self.period_list = deque(maxlen=30)  # Use deque to store the last 30 periods
        
        self.period = 0
        #incializacion de pines como entradas
        GPIO.setmode(GPIO.BCM)  
        GPIO.setup(self.pin_a, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.pin_b, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        #estados iniciales de los pines
        self.last_A = GPIO.input(self.pin_a)
        self.last_B = GPIO.input(self.pin_b)
        self.last_position = self.last_A 

        #configuracion para disparar funcion Callback() en cada flanco positivo de cada entrada
        GPIO.add_event_detect(self.pin_a, GPIO.BOTH, callback=self.encoder_callback)
        GPIO.add_event_detect(self.pin_b, GPIO.BOTH, callback=self.encoder_callback)

    #funcion que se dispara cada vez que se detecta un flanco alto en las entradas de senales de la Raspberry Pi
    #entradas: pulsos altos de las senales
    #salidas: periodo de rotacion del encoder
    def encoder_callback(self, channel):

        #se actualizan los estados de los pines de entrada
        A = GPIO.input(self.pin_a)
        B = GPIO.input(self.pin_b)

        #se toma tiempo incial con 0 pulsos contados   
        if self.pulse_count == 0:
            self.rotation_start_time = time.time()
        
        #en cada cambio de estado, se anade 1 a los pulsos contados
        if A != self.last_A or B != self.last_B:
            self.pulse_count += 1
            self.last_A = A
            self.last_B = B


        #una vez que se alcanza el numero de pulsos por rotacion requerido
        #se calcula el tiempo transcurrido en la rotacion completa
        if self.pulse_count >= self.ppr:
            self.rotation_end_time = time.time()
            period = self.rotation_end_time - self.rotation_start_time
            self.period_list.append(period)  # Add the new period to the list
            self.pulse_count = 0

    #promedia el periodo en varias mediciones para reducir picos
    #entrads: lista que contiene los ultimos 30 valores medidos
    def get_average_period(self):
        if len(self.period_list) == 0:
            return 0
        return sum(self.period_list) / len(self.period_list)

    #funcio npar areinicar las entrads de GPIO
    def cleanup(self):
        GPIO.cleanup()

