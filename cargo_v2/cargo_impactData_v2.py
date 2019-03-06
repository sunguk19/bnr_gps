import requests, json, time
import RPi.GPIO as GPIO

dataPin = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(dataPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
time.sleep(1)

i_url = "http://bnrtracker.qroo.co.kr/_API/saveImpactData.php"
dev_num = "cargo_proto0"

while True :

    result = GPIO.input(dataPin)

    if result == 1:
        try :
            params = {}
            params['device_number'] = dev_num
            now = time.localtime()
            datetime = str(now.tm_year) + "-" + str(now.tm_mon) + "-" + str(now.tm_mday) + "-" + str(now.tm_hour) + "-" + str(now.tm_min) + "-" + str(now.tm_sec)
            params['tra_datetime'] = datetime
            params['tra_impact'] = result
            
            dataString = ""
            dataString = dataString + str(dev_num)
            dataString = dataString + " * * * * * * * * "
            dataString = dataString + str(params['tra_datetime']) + " * * " + str(result) + "\n"
            f = open("./DATA.txt", 'a+')
            f.write(dataString)
            f.close()
            #res = requests.post(url = i_url, data = params)
            #print(res.json())
            print (dataString)


        except : 
            print("fail to post impact")
