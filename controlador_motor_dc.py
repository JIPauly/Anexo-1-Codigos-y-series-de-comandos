
import RPi.GPIO as GPIO
from time import sleep


#se definene los pines de salida de control del controlador L298N
#tanto como los pines de comunicacion con la Raspberry Pi para enable (en) 
in1 = 24
in2 = 23
en = 25
temp1=1


#configuracion I/O de cada pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)

#frecuencia de funcionamiento de la pwm
p=GPIO.PWM(en,2000)

p.start(25)
print("\n")
print("motor inicializado, escoja la frecuecencia a usar")
print("\n")


#menu de seleccion de estado de motor
# el procentaje de opracion se obtiene de la frecuecnia nominal sin carga del motor
#es decir, a un ciclo de trabajo del 100%, el motor opera a 36 Hz
while(1):

    x=input()
    #enciendido del motor
    if x=='r':
        print("correr")
        if(temp1==1):
         GPIO.output(in1,GPIO.HIGH)
         GPIO.output(in2,GPIO.LOW)
         print("horario")
         x='z'
        else:
         GPIO.output(in1,GPIO.LOW)
         GPIO.output(in2,GPIO.HIGH)
         print("antihorario")
         x='z'
    #paro del motor
    elif x=='s':
        print("alto")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        x='z'
    #cmabio a sentido horario
    elif x=='f':
        print("horario")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        temp1=1
        x='z'
    #cambio a sentido anti horario
    elif x=='b':
        print("anti horario")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        temp1=0
        x='z'


    #empiezan las opciones para selecion de regimen de trabajo.

    #formula utilizada: 

    #Regimen de trabajo = x/36 donde x son los hz de salida deseados
    elif x=='1':
        print("5 hz")
        p.ChangeDutyCycle(13.889)
        x='z'

    elif x=='2':
        print("10 hz")
        p.ChangeDutyCycle(27.778)
        x='z'

    elif x=='3':
        print("15 hz")
        p.ChangeDutyCycle(41.667)
        x='z'

    elif x=='3':
        print("20 hz")
        p.ChangeDutyCycle(55.556)
        x='z'

    elif x=='4':
        print("25 hz")
        p.ChangeDutyCycle(69.444)
        x='z'

    elif x=='5':
        print("30 hz")
        p.ChangeDutyCycle(83.333)
        x='z'


    #salida del script
    elif x=='e':
        GPIO.cleanup()
        print("GPIO Clean up")
        break


    #caso de excepcion si el usiario ingresa un comando no valido
    else:
        print("<<<  error >>>")
        print("por favor ingrese un codigo valido.....")
