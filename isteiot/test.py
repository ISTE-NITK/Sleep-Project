import serial
port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=8.0)
port.close()
port.open()
while True:
    rcv=port.readline()
    print(str(rcv))
