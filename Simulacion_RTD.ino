#include <Wire.h> //Arduino Uno; SDA = A4, SCL = A5
#include <SPI.h>
//CS => CS //Arduino 10
//MISO (master in slave out) => SDO //Arduino 12
//MOSI (master out slave in) => SDI //Arduino 11
//SCK => SCLK //Arduino 13

//Variable del PT100
double resistance;
uint8_t reg1, reg2; //reg1 tiene el Bit mas significativo, reg2 tiene le bit menos significativo
uint16_t fullreg; //registros combinadso
double temperature;
//Variables usadas para las ecuacionas de Van Dusen
double Z1, Z2, Z3, Z4, Rt;
double RTDa = 3.9083e-3;
double RTDb = -5.775e-7;
double rpoly = 0;



const int chipSelectPin = 10; //Se usa para dar senal baja a MAX para empezar comunicacion



void setup()
{
  SPI.begin();
  Serial.begin(9600); //Empieza monitor serial
  pinMode(chipSelectPin, OUTPUT); //Se selecciona el pin CS como output debido a que este debe ser activado manualmente para iniciar comunicacion
                                  // Con MAX31865
}

void loop()
{
  readRegister();
  convertToTemperature();
  delay(1000);
}


void convertToTemperature()
{
  Rt = resistance;
  Rt /= 32768;
  Rt *= 430; //Se usa el valor leido del registro con la formula de la hoja de datos
  //para encontrar el valor de la ressitencia del rtd

  Z1 = -RTDa;
  Z2 = RTDa * RTDa - (4 * RTDb);
  Z3 = (4 * RTDb) / 100;
  Z4 = 2 * RTDb;

  temperature = Z2 + (Z3 * Rt);
  temperature = (sqrt(temperature) + Z1) / Z4;

  if (temperature >= 0)
  {
    Serial.print("Temperatura del aciete: ");
    Serial.println(temperature); //Temperatura en Celsius
    return; 
  }
  else
  {
    Rt /= 100;
    Rt *= 100; 

    rpoly = Rt;

    temperature = -242.02;
    temperature += 2.2228 * rpoly;
    rpoly *= Rt; // ^2
    temperature += 2.5859e-3 * rpoly;
    rpoly *= Rt; // ^3
    temperature -= 4.8260e-6 * rpoly;
    rpoly *= Rt; // ^4
    temperature -= 2.8183e-8 * rpoly;
    rpoly *= Rt; // ^5
    temperature += 1.5243e-10 * rpoly;

    //Serial.print("Temperature: ");
    //Serial.println(temperature); //tempe en grados Celsius 
  }
  //Note: all formulas can be found in the AN-709 application note from Analog Devices
}


void readRegister()
{
  SPI.beginTransaction(SPISettings(500000, MSBFIRST, SPI_MODE1));
  digitalWrite(chipSelectPin, LOW);//Envia senal apra empezar transmision


  SPI.transfer(0x80); //80h = 128 - Accede al regirto de configuracion
  SPI.transfer(0xB0); //B0h = 176 - 10110000: bias ON, 1-shot, start 1-shot, 3-wire, el resto son 0. Esta es la confguracion de los datos a extraer
  // 
  digitalWrite(chipSelectPin, HIGH);

  digitalWrite(chipSelectPin, LOW);


  SPI.transfer(1); // Se envia un 1 para indicar que se quiere leer el primer registro
  reg1 = SPI.transfer(0xFF); //se inicializan las variables de registro
  reg2 = SPI.transfer(0xFF);
  digitalWrite(chipSelectPin, HIGH);

  fullreg = reg1; //leer BMS
  fullreg <<= 8;  //mover a la izquierda, para que sea el BMS
  fullreg |= reg2; //Leer bit menos significativo, y combinar con mas significativo
  fullreg >>= 1; //se desecha D0 del registro, la hoja de datos indica que esto es necesario
  resistance = fullreg; //se asigna la direccion de registro al valor de resistencia

  digitalWrite(chipSelectPin, LOW);

  SPI.transfer(0x80); //80h = 128
  SPI.transfer(144); //144 = 10010000
  SPI.endTransaction();
  digitalWrite(chipSelectPin, HIGH);

  Serial.print("La resisntencia del sensor RTD es: ");
  Serial.println(resistance);
}