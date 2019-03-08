import requests, json, time
import RPi.GPIO as GPIO

dataPin = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(dataPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
time.sleep(1)

while True :

    result = GPIO.input(dataPin)

    if result == 1:
        try :
            now = time.localtime()
            datetime = str(now.tm_year) + "-" + str(now.tm_mon) + "-" + str(now.tm_mday) + "-" + str(now.tm_hour) + "-" + str(now.tm_min) + "-" + str(now.tm_sec)
            
            dataString = "BNRtechnology_cargo_tracker_Idata"
            dataString = dataString + " * * * * * * * * "
            dataString = dataString + str(datetime) + " * * " + str(result) + "\n"
            f = open("./DATA.txt", 'a+')
            f.write(dataString)
            f.close()
            print (dataString)


        except : 
            print("fail to post impact")
