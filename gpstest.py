import serial
import pynmea2

port = '/dev/ttyAMA0'
ser = serial.Serial(port, baudrate =  9600)
print ("serial is connected")

while True :
    data = ser.readline()
    print data
    if data[0:6] == '$GPGGA' :
        msg = pynmea2.parse(data)
        print(msg.lat + msg.lon)

