#include <MQ135.h>    //Air Quality Sensor: 
#include <dht.h>      //Temperature and Humidity Sensor: http://www.circuitbasics.com/wp-content/uploads/2015/10/DHTLib.zip

#define AIRQUALITYPIN A0
#define DHT11_PIN 2

dht DHT;
MQ135 gasSensor = MQ135(AIRQUALITYPIN);

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  float rzero = gasSensor.getRZero();
  float ppm = gasSensor.getPPM();
  
  Serial.println(ppm);
  int chk = DHT.read11(DHT11_PIN);
  //Serial.print("Temperature = ");
  Serial.println(DHT.temperature);
  //Serial.print("Humidity = ");
  Serial.println(DHT.humidity);
  delay(10000);
}

