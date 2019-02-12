import RPi.GPIO as GPIO
import time
import datetime
datapin = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(datapin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
time.sleep(1)

while True:
    result = GPIO.input(datapin)
    if result == 1:
        s = datetime.datetime.now()
        print s
        print("detected")
        time.sleep(0.5)
