import requests, json, time
import RPi.GPIO as GPIO

dataPin = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(dataPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
time.sleep(1)

de_number = "cargo_proto0"
log_files_path = "/home/pi/gpstracker/cargo_v5/log_files/"

data_buffer=[]

while True :
    params = {}
    result = GPIO.input(dataPin)
    if result == 1:
        params['tra_impact'] = 1
        params['de_number'] = de_number
        #try :
        now = time.localtime()
        datetime = str(now.tm_year) + "-" + str(now.tm_mon) + "-" + str(now.tm_mday) + "-" + str(now.tm_hour) + "-" + str(now.tm_min) + "-" + str(now.tm_sec)
        params['tra_datetime'] = datetime
        dataString = de_number
        dataString = dataString + " * * * * * * * * "
        dataString = dataString + str(datetime) + " * * " + str(result) + "\n"
        print (dataString)
        data_buffer.append(params)
        with open(log_files_path + datetime + "i.json", "a+") as make_file:
            json.dump(params, make_file, ensure_ascii = False, indent = '\t')
        time.sleep(0.5)




