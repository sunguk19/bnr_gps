import serial
import pynmea2
import Adafruit_DHT
import smbus            #import SMBus module of I2C
from time import sleep          #import
import datetime
import requests, json, time
import subprocess
import serial

#proc = subprocess.Popen("sudo python3 /home/pi/bnr_gps/cargo_v6/cargo_impactData_v6.py", stdout = subprocess.PIPE, shell = True)
#proc1= subprocess.Popen("sudo python /home/pi/bnr_gps/cargo_v6/cargo_post_v6.py", stdout = subprocess.PIPE, shell = True)

de_number = "cargo_proto0"
log_files_path = "/home/pi/bnr_gps/cargo_v6/log_files/"


temp_sensor = Adafruit_DHT.DHT22
temp_pin = 4
gps_port = '/dev/ttyAMA0'


gps_ser = serial.Serial(gps_port, baudrate =  9600, timeout = 2)
print ("GPS serial is connected")
data_buffer=[]

while True :

    params = {} 
    params['de_number'] = str(de_number)
    for i in range (0,20) :
        gps_data = gps_ser.readline()
        if gps_data[0:6] == b'$GNGGA' :
            print ("find GNGGA")
            break


    
    try : 
        if gps_data[0:6] == b'$GNGGA' :
            msg = pynmea2.parse(gps_data.decode("utf-8","ignore"))
            print (msg.lat)
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
            print ("else")
            params['tra_lat'] = "*****"
            params['tra_lon'] = "*****"
    except : 
        params['tra_lat'] = "*****"
        params['tra_lon'] = "*****"
    
    params['tra_Ax'] = 0
    params['tra_Ay'] = 0
    params['tra_Az'] = 0

    params['tra_Gx'] = 0
    params['tra_Gy'] = 0
    params['tra_Gz'] = 0

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

    dataString = str(params['de_number']) + " " + str(params['tra_temp']) + " " + str(params['tra_humidity']) + " " + str(params['tra_Gx']) + " " + str(params['tra_Gy']) + " " + str(params['tra_Gz']) + " " + str(params['tra_Ax']) + " " + str(params['tra_Ay']) + " " + str(params['tra_Az']) + " " + str(params['tra_datetime']) + " " + str(params['tra_lat']) + " " + str(params['tra_lon']) + " 0\n"

    print (dataString)
    data_buffer.append(params)
    time.sleep(1)
    if len(data_buffer) > 5 :
        with open(log_files_path + datetime + "r.json", 'a') as make_file:
            json.dump(data_buffer,make_file,  ensure_ascii = False, indent = "\t")
        data_buffer=[]

