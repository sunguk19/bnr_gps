import serial
import time
ser = serial.Serial("/dev/ttyACM0", 9600,timeout = 15)
#time.sleep(1)
ser.write("at+kusbcomp?\r\n")
print ser.readline()
print ser.readline()
time.sleep(1)
#ser.write("at+cgreg=0,1\r\n")
#print ser.readline()
#print ser.readline()
#time.sleep(2)
ser.write("at+cgdcont=1, \"IP\", \"internet.swir\"\r\n")
print ser.readline()
print ser.readline()
time.sleep(2)
ser.write("at+xdns=1,1\r\n")
print ser.readline()
print ser.readline()
time.sleep(2)
ser.write("at+xcedata=1,0\r\n")
print ser.readline()
print ser.readline()
time.sleep(2)
ser.write("at+xcedata=1,1\r\n")
print ser.readline()
print ser.readline()
time.sleep(2)
ser.close()
exit()
