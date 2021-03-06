import serial
import pynmea2
import Adafruit_DHT
import smbus            #import SMBus module of I2C
from time import sleep          #import
import datetime
import requests, json, time
import subprocess
import serial

proc = subprocess.Popen("sudo python3 /home/pi/bnr_gps/cargo_v5/cargo_impactData_v5.py", stdout = subprocess.PIPE, shell = True)
proc1= subprocess.Popen("sudo python /home/pi/bnr_gps/cargo_v5/cargo_post_v5.py", stdout = subprocess.PIPE, shell = True)

de_number = "cargo_proto0"
log_files_path = "/home/pi/bnr_gps/cargo_v5/log_files/"


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

gps_ser = serial.Serial(gps_port, baudrate =  9600, timeout = 2)
print ("GPS serial is connected")
data_buffer=[]

while True :

    gps_data = gps_ser.readline()
    params = {} 
    params['de_number'] = str(de_number)
    for i in range (0,7) :
        gps_data = gps_ser.readline()
        if gps_data[0:6] == '$GPGGA' :
            break


    
    try : 
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

        else :
            params['tra_lat'] = "*****"
            params['tra_lon'] = "*****"
    except : 
        params['tra_lat'] = "*****"
        params['tra_lon'] = "*****"

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
    
    params['tra_Ax'] = round(Ax, 3)
    params['tra_Ay'] = round(Ay, 3)
    params['tra_Az'] = round(Az, 3)

    params['tra_Gx'] = round(Gx, 3)
    params['tra_Gy'] = round(Gy, 3)
    params['tra_Gz'] = round(Gz, 3)

    now = time.localtime()
    datetime = str(now.tm_year) + "-" + str(now.tm_mon) + "-" + str(now.tm_mday) + "-" + str(now.tm_hour) + "-" + str(now.tm_min) + "-" + str(now.tm_sec)
    params['tra_datetime'] = datetime
    
    humidity, temperature = Adafruit_DHT.read_retry(temp_sensor, temp_pin)
    if humidity is not None and temperature is not None:
        params['tra_temp'] = temperature
        params['tra_humidity'] = humidity
    else :
        params['tra_temp'] = "******"
        params['tra_humidity'] = "******"
    """ 
    params['tra_temp'] = "******"
    params['tra_humidity'] = "******" 
    """    
    dataString = str(params['de_number']) + " " + str(params['tra_temp']) + " " + str(params['tra_humidity']) + " " + str(params['tra_Gx']) + " " + str(params['tra_Gy']) + " " + str(params['tra_Gz']) + " " + str(params['tra_Ax']) + " " + str(params['tra_Ay']) + " " + str(params['tra_Az']) + " " + str(params['tra_datetime']) + " " + str(params['tra_lat']) + " " + str(params['tra_lon']) + " 0\n"

    print (dataString)
    data_buffer.append(params)
    time.sleep(1)
    if len(data_buffer) > 5 :
        with open(log_files_path + datetime + "r.json", 'a') as make_file:
            json.dump(data_buffer,make_file,  ensure_ascii = False, indent = "\t")
        data_buffer=[]

