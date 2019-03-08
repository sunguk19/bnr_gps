import time
import requests, json

d_url = "https://bnrtracker.dreammug.com/_API/saveData.php"
i_url = "https://bnrtracker.dreammug.com/_API/saveDataImpact.php"

de_number = "cargo_proto0"


while 1:
    f = open("/home/pi/gpstracker/cargo_v2/DATA.txt", "a+")
    l = f.readlines()
    f.close()

    if len(l) < 1:
        print "data is not exist"
        time.sleep(1)
    else :
        line = str(l[0])
        line = line.split()
        print line

        params = {'de_number' : line[0], 'tra_temp' : line[1], 'tra_humidity' : line[2], 'tra_Gx' : line[3], 'tra_Gy' : line[4], 'tra_Gz' : line[5], 'tra_Ax' : line[6], 'tra_Ay' : line[7], 'tra_Az' : line[8], 'tra_datetime' : line[9], 'tra_lat' : line[10], 'tra_lon' : line[11], 'tra_impact' : line[12]}
        
        try : 
            if params['tra_impact'] == 0 :
                res = requests.post(url = d_url, data = params)
            else :
                res = requests.post(url = i_url, data = params)
        except : 
            print "fail to post"

        del l[0]
        f = open("/home/pi/gpstracker/cargo_v2/DATA.txt", "w")
        f.writelines(l)
        f.close()

