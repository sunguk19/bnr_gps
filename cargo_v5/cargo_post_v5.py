import json, requests
import os, time

d_url = "http://bnrtracker.dreammug.com/_API/uploadFile.php"
log_data_path = "/home/pi/gpstracker/cargo_v5/log_files/"


while 1:
    try : 
        file_list = os.listdir(log_data_path)
        print len(file_list)
        if len(file_list) > 0 :
            #proc = subprocess.Popen("sudo python /home/pi/gpstracker/cargo_v5/ser.py", stdout = subprocess.PIPE, shell = True)
            for i in range(0, len(file_list)) :
                files = {'logFile' : open(log_data_path + str(file_list[i]), 'rb')}
                res = requests.post(url = d_url, files = files)
                print res.json()
                if res.json()["status_code"] == "0" :
                    os.remove(log_data_path + str(file_list[i]))
                    print "del"
        else :
            print "no file"
            time.sleep(1)
    except : 
        pass
        time.sleep(1)
