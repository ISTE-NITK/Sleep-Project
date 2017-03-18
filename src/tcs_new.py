
import smbus
import time
import numpy as np
import serial
import datetime
import pytz

#Arduino RX 0 -> RPi 14 
#Arduino TX 1 -> RPi 15
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=0)

#SDA GPIO P3
#SCL GPIO P5

bus = smbus.SMBus(1)
# I2C address 0x29
# Register 0x12 has device ver. 
# Register addresses must be OR'ed with 0x80
bus.write_byte(0x29,0x80|0x12)
ver = bus.read_byte(0x29)

# version # should be 0x44
if ver == 0x44:
 print "Device found\n"
 bus.write_byte(0x29, 0x80|0x00) # 0x00 = ENABLE register
 bus.write_byte(0x29, 0x01|0x02) # 0x01 = Power on, 0x02 RGB sensors enabled
 bus.write_byte(0x29, 0x80|0x14) # Reading results start register 14, LSB then MSB
 
 f=open('csv_data.csv', 'ab')
 f.write("airquality, clear, red, green, blue, illuminance, timestamp\n")
 f.close() #Columns of CSV file (sensor readings + timestamp)
 
 while True:
  data = bus.read_i2c_block_data(0x29, 0)
  clear = clear = data[1] << 8 | data[0]
  red = data[3] << 8 | data[2]
  green = data[5] << 8 | data[4]
  blue = data[7] << 8 | data[6]
  illuminance=(-0.32466*red)+(1.57837*green)+(-0.73191*blue)
  #Converts raw r/g/b values to luminosity in lux
  
  crgbi = "%s, %s, %s, %s, %s, " % (clear, red, green, blue,illuminance)
  
  f=open('csv_data.csv','ab')

  value = ser.readline().decode('utf-8')
  if value:  # If it isn't a blank line
  	f.write(value.rstrip() + ", ")
	#strip newline from Arduino 
  f.write(crgbi)
  utc_time = datetime.datetime.now(pytz.utc)
  local_time = (utc_time.astimezone(pytz.timezone('Asia/Calcutta')))
  f.write(str(local_time))
  f.write("\n")
  print crgbi
  f.close()

  time.sleep(10) 
  #sampling time between readings 
 
else: 
 print "Device not found\n"
