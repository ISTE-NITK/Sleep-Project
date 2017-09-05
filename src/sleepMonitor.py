
import smbus
import time
import numpy as np
import serial
import datetime
import pytz

#Arduino RX 0 -> RPi 14 
#Arduino TX 1 -> RPi 15
ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=0)

#SDA GPIO P3
#SCL GPIO P5

bus = smbus.SMBus(1)
# I2C address 0x29
# Register 0x12 has device ver. 
# Register addresses must be OR'ed with 0x80
bus.write_byte(0x29,0x80|0x12)
ver = bus.read_byte(0x29)

utc_time = datetime.datetime.now(pytz.utc)
local_time = (utc_time.astimezone(pytz.timezone('Asia/Calcutta')))
date = (str(local_time)).split()[0]


# version # should be 0x44
if ver == 0x44:
 print "********************************************************************************"
 print "********************************************************************************"
 print "                                                                                       "
 print "                            SLEEP RECORDING INITIATED                                  "
 print "                                                                                       "
 print "                                 ON "+date+". "
 print " "                                                                                     
 print "                          Hit Ctrl+C to exit application."
 print " "
 print " "
 print "********************************************************************************"
 print "********************************************************************************"
 print " "
 time.sleep(10)  
	
 bus.write_byte(0x29, 0x80|0x00) # 0x00 = ENABLE register
 bus.write_byte(0x29, 0x01|0x02) # 0x01 = Power on, 0x02 RGB sensors enabled
 bus.write_byte(0x29, 0x80|0x14) # Reading results start register 14, LSB then MSB

 

 f=open('/home/pi/Desktop/'+ date +'_data.csv', 'ab')
 f.write("airquality, temperature, humidity, clear, red, green, blue, illuminance, timestamp\n")
 f.close() #Columns of CSV file (sensor readings + timestamp)
 
 while True:
  data = bus.read_i2c_block_data(0x29, 0)
  clear = clear = data[1] << 8 | data[0]
  red = data[3] << 8 | data[2]
  green = data[5] << 8 | data[4]
  blue = data[7] << 8 | data[6]
  illuminance=(-0.32466*red)+(1.57837*green)+(-0.73191*blue)
  #Converts raw r/g/b values to luminosity in lux
  
  crgbi = "%s, %s, %s, %s, %s, " % (clear, red, green, blue, illuminance)
  
  utc_time = datetime.datetime.now(pytz.utc)
  local_time = (utc_time.astimezone(pytz.timezone('Asia/Calcutta')))
  date = (str(local_time)).split()[0]

  f=open('/home/pi/Desktop/'+ date +'_data.csv','ab')

  quality = ser.readline().decode('utf-8')
  if quality:  # If it isn't a blank line
  	f.write(quality.rstrip() + ", ")
  else:
 	print "Error: Check Air Quality Sensor Connections.\n"

  celsius = ser.readline().decode('utf-8')
  if celsius:  # If it isn't a blank line
    f.write(celsius.rstrip() + ", ")  
  else:
    print "Error: Check Temperature & Humidity Sensor Connections.\n"
	  
  humid = ser.readline().decode('utf-8')
  if humid:  # If it isn't a blank line
    f.write(humid.rstrip() + ", ")
  #strip newline from Arduino 
  
  f.write(crgbi)
  #print date
  f.write(str(local_time))
  f.write("\n")
  #print "Data Stored!"
  f.close()

  time.sleep(10) 
  #sampling time between readings 
 
else: 
 print "Error: Light Sensor not found\n"
