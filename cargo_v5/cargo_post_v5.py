import json, requests, subprocess
import os, time

#d_url = "http://bnrtracker.dreammug.com/_API/uploadFile.php"
d_url = "http://bnrtracker.dreammug.com/_API/saveDataFromJson.php"
#log_data_path = "/home/pi/bnr_gps/cargo_v5/log_files_test/"
log_data_path = "/home/pi/bnr_gps/cargo_v5/log_files/"

proc = subprocess.Popen("sudo python /home/pi/bnr_gps/cargo_v5/ser.py", stdout = subprocess.PIPE, shell = True)

while 1:
    try : 
        file_list = os.listdir(log_data_path)
        print len(file_list)
        if len(file_list) > 0 :
            #proc = subprocess.Popen("sudo python /home/pi/bnr_gps/cargo_v5/ser.py", stdout = subprocess.PIPE, shell = True)
            for i in range(0, len(file_list)) :
                if os.path.getsize(log_data_path + str(file_list[i])) <= 0 :
                    print str(file_list[i]) + " is empty pass to next file"
                    os.remove(log_data_path + str(file_list[i]))
                    continue
                
                files = {'logFile' : open(log_data_path + str(file_list[i]), 'rb')}
                res = requests.post(url = d_url, files = files)
                print log_data_path + str(file_list[i]) 
                if res.json()["status_code"] == "0" :
                    os.remove(log_data_path + str(file_list[i]))
                    print "del"
                else :
                    pass
                    proc = subprocess.Popen("sudo python /home/pi/bnr_gps/cargo_v5/ser.py", stdout = subprocess.PIPE, shell = True)
        else :
            print "no file"
            time.sleep(1)
    except :
        print "error"
        pass
        time.sleep(1)
