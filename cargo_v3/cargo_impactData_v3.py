import requests, json, time
import RPi.GPIO as GPIO

dataPin = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(dataPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
time.sleep(1)

de_number = "cargo_proto0"
idata_path = "/home/pi/gpstracker/cargo_v3/Idata.txt" 
#i_url = "http://bnrtracker.dreammug.com/_API/saveImpactData.php"
i_url = "http://bnrtracker.dreammug.com/_API/saveData.php"

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
"""
        f = open(idata_path, 'a+')
        f.write(dataString)
        f.close()
        print (dataString)
            
    f = open(idata_path, "r")
    l = f.readlines()
    f.close()
    
    while len(l) > 1 :
        line = str(l[0])
        line = line.split()
        print line

        idata = {'de_number' : line[0], 'tra_temp' : line[1], 'tra_humidity' : line[2], 'tra_Gx' : line[3], 'tra_Gy' : line[4], 'tra_Gz' : line[5], 'tra_Ax' : line[6], 'tra_Ay' : line[7], 'tra_Az' : line[8], 'tra_datetime' : line[9], 'tra_lat' : line[10], 'tra_lon' : line[11], 'tra_impact' : line[12]}

        try : 
            res = requests.post(url = i_url, data = idata)
            aaa = str(res.json()).split()
            print aaa[1]
        except : 
            print "fail to post"
            aaa = ["0", "0"]
        if aaa[1] == "True," :
            del l[0]
        else :
            break
    f = open(idata_path, "w")
    f.writelines(l)
    f.close()

"""
        
        #except : 
        #    print("fail to post impact")
