
import smbus
import time
import numpy as np

import datetime
import pytz

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
 while True:
  data = bus.read_i2c_block_data(0x29, 0)
  clear = clear = data[1] << 8 | data[0]
  red = data[3] << 8 | data[2]
  green = data[5] << 8 | data[4]
  blue = data[7] << 8 | data[6]
  crgb = "C: %s, R: %s, G: %s, B: %s\n" % (clear, red, green, blue)
  crgb_array= np.array([clear, red, green, blue])
  f=open('csv_data.dat','ab')
  np.savetxt(f, crgb_array)
  utc_time = datetime.datetime.now(pytz.utc)
  local_time = (utc_time.astimezone(pytz.timezone('Asia/Calcutta')))
  f.write(str(local_time))
  print crgb
  f.close()
  time.sleep(10)
else: 
 print "Device not found\n"
