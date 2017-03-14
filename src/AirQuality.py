import serial
import time
from datetime import datetime
ser = serial.Serial('COM3', 9600, timeout=0)
while 1:
   try:
        print(str(datetime.now())+' ')
        value = ser.readline().decode('utf-8')
        print(value)
        f = open('F:\output.txt', 'a+')	
        if value:  # If it isn't a blank line
            f.write(str(datetime.now())+'\t')
            f.write(value)
   except ser.SerialTimeoutException:
        print('Data could not be read')
   time.sleep(60)
f.close()