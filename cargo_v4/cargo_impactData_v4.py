import requests, json, time
import RPi.GPIO as GPIO

dataPin = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(dataPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
time.sleep(1)

de_number = "cargo_proto0"
log_files_path = "/home/pi/gpstracker/cargo_v4/log_files/"


while True :

    result = GPIO.input(dataPin)
    if result == 1:
        #try :
        now = time.localtime()
        datetime = str(now.tm_year) + "-" + str(now.tm_mon) + "-" + str(now.tm_mday) + "-" + str(now.tm_hour) + "-" + str(now.tm_min) + "-" + str(now.tm_sec)
            
        dataString = de_number
        dataString = dataString + " * * * * * * * * "
        dataString = dataString + str(datetime) + " * * " + str(result) + "\n"
        print (dataString)
        f = open(log_files_path + datetime + "i" + ".txt", "a+")
        f.write(dataString)
        f.close()
        time.sleep(0.5)




