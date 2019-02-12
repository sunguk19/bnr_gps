import subprocess
import os
import time

proc = subprocess.Popen("python sw.py", stdout=subprocess.PIPE, shell=True)

while True :
    out, err = proc.communicate()
    print out
    print "test"
    time.sleep(0.5)


