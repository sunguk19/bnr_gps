import json, requests
import os

d_url = "http://bnrtracker.dreammug.com/_API"
log_data_path = "/home/pi/gpstracker/cargo_v5/log_files/"

file_list = os.listdir(log_data_path)
print file_list
files = {'myfile' : open(log_data_path + str(file_list[0]), 'rb')}
res = requests.post(url = d_url, data = files)
print (res)
