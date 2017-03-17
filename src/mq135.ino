#include <MQ135.h>

#define ANALOGPIN A0

MQ135 gasSensor = MQ135(ANALOGPIN);

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  float rzero = gasSensor.getRZero();
  float ppm = gasSensor.getPPM();
  Serial.println(ppm);
  delay(10000);
}

