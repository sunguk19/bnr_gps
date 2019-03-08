import serial
import pynmea2
import Adafruit_DHT
import smbus            #import SMBus module of I2C
from time import sleep          #import
import datetime
import requests, json, time
import subprocess

proc = subprocess.Popen("sudo python /home/pi/gpstracker/cargo_impactData_v2.py", stdout = subprocess.PIPE, shell = True)


d_url = "http://bnrtracker.qroo.co.kr/_API/saveData.php"
i_url = "http://bnrtracker.qroo.co.kr/_API/saveImpactData.php"

dev_num = "cargo_proto0"

temp_sensor = Adafruit_DHT.DHT22
temp_pin = 4
gps_port = '/dev/ttyAMA0'

PWR_MGMT_1 = 0x6b
SMPLRT_DIV = 0X19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
INT_ENABLE = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47


def MPU_Init() :
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
    bus.write_byte_data(Device_Address, CONFIG, 0)
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr) :
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr + 1)

    value = ((high << 8) | low)
    if(value > 32768):
        value = value - 65536
    return value

bus = smbus.SMBus(1)
Device_Address = 0x68

MPU_Init()
print ("start gyro")

gps_ser = serial.Serial(gps_port, baudrate =  9600, timeout = 1)
print ("serial is connected")

while True :

    params = {}
    params['device_number'] = dev_num

    gps_data = gps_ser.readline()
#    print gps_data

   # while gps_data[0:6] != '$GPGGA' :
    #    gps_data = gps_ser.readline()
    
    for i in range (0,7) :
        gps_data = gps_ser.readline()
        if gps_data[0:6] == '$GPGGA' :
            break


    

    if gps_data[0:6] == '$GPGGA' :
        msg = pynmea2.parse(gps_data)
        if msg.lat == "" :
            msg.lat = "0.0"
        b = eval(msg.lat) / 100
        a = str(b).split(".")
        clat = a[0] + "." + str(eval(a[1]) / 60)
        if msg.lon == "" :
            msg.lon = "0.0"
        z = eval(msg.lon) / 100
        x = str(z).split(".")
        clon = x[0] + "." + str(eval(x[1]) / 60)
        params['tra_lat'] = str(clat)
        params['tra_lon'] = str(clon)
        if params['tra_lat'] == "0.0" : 
            params['tra_lat'] = "*****"
        if params['tra_lon'] == "0.0" : 
            params['tra_lon'] = "*****"

#        print("lat : " + clat + "             " +  "lon = " + clon)
    else :
        params['tra_lat'] = "*****"
        params['tra_lon'] = "*****"

    #else :
       # print("gps dectection is fail")
    acc_x = read_raw_data(ACCEL_XOUT_H)
    acc_y = read_raw_data(ACCEL_YOUT_H)
    acc_z = read_raw_data(ACCEL_ZOUT_H)
    gyro_x = read_raw_data(GYRO_XOUT_H)
    gyro_y = read_raw_data(GYRO_YOUT_H)
    gyro_z = read_raw_data(GYRO_ZOUT_H)
    
    Ax = acc_x / 16384.0
    Ay = acc_y / 16384.0
    Az = acc_z / 16384.0

    Gx = gyro_x / 131.0
    Gy = gyro_y / 131.0
    Gz = gyro_z / 131.0
    
    params['tra_Ax'] = Ax
    params['tra_Ay'] = Ay
    params['tra_Az'] = Az

    params['tra_Gx'] = Gx
    params['tra_Gy'] = Gy
    params['tra_Gz'] = Gz
    #params['tra_impact'] = NULL
    #s = datetime.datetime.now()
    #print s
    now = time.localtime()
    datetime = str(now.tm_year) + "-" + str(now.tm_mon) + "-" + str(now.tm_mday) + "-" + str(now.tm_hour) + "-" + str(now.tm_min) + "-" + str(now.tm_sec)
    params['tra_datetime'] = datetime

 #   print("Gx = %.2fdeg/s"%Gx + " Gy = %.2fdeg/s"%Gy, "Gz = %.2fdeg/s"%Gz, "Ax = %.2fg"%Ax, "Ay = %.2fg"%Ay, "Az = %.2fg"%Az)
    #print("Gx = %.3fdeg/s"%Gx + " Gy = %.3fdeg/s"%Gy, "Gz = %.3fdeg/s"%Gz, "Ax = %.3fg"%Ax, "Ay = %.3fg"%Ay, "Az = %.3fg"%Az)


    humidity, temperature = Adafruit_DHT.read_retry(temp_sensor, temp_pin)
    if humidity is not None and temperature is not None:
  #      print('Temp = {0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        params['tra_temp'] = temperature
        params['tra_humidity'] = humidity
    else :
   #     print('fail to get reading temperature sensor value')
        params['tra_temp'] = "******"
        params['tra_humidity'] = "******"
    
  #  try :
    dataString = str(dev_num) + " " + str(params['tra_temp']) + " " + str(params['tra_humidity']) + " " + str(params['tra_Gx']) + " " + str(params['tra_Gy']) + " " + str(params['tra_Gz']) + " " + str(params['tra_Ax']) + " " + str(params['tra_Ay']) + " " + str(params['tra_Az']) + " " + str(params['tra_datetime']) + " " + str(params['tra_lat']) + " " + str(params['tra_lon']) + " 0\n"

    print (dataString)
    f = open("/home/pi/gpstracker/DATA.txt", "a+")
    f.write(dataString)
    f.close()




        #res = requests.post(url = d_url, data = params)
        #print(res.json())
    #except :
     #   print("fail to post")


