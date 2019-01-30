import serial
import pynmea2
import Adafruit_DHT

temp_sensor = Adafruit_DHT.DHT22
temp_pin = 4

gps_port = '/dev/ttyAMA0'
gps_ser = serial.Serial(gps_port, baudrate =  9600)
print ("serial is connected")

while True :
    gps_data = gps_ser.readline()
#    print gps_data
    if gps_data[0:6] == '$GPGGA' :
        msg = pynmea2.parse(gps_data)
        print(msg.lat + msg.lon)
    else :
        print("gps dectection is fail")
    humidity, temperature = Adafruit_DHT.read_retry(temp_sensor, temp_pin)
    if humidity is not None and temperature is not None:
        print('Temp = {0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
    else :
        print('fail to get reading temperature sensor value')

