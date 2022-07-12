import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)   #采用BCM编码
GPIO.setup(5,GPIO.OUT)   #指定使用5号编口
GPIO.setup(6,GPIO.OUT) 
for i in range(1,10):
    GPIO.output(5,GPIO.HIGH)
    GPIO.output(6,GPIO.HIGH)
    sleep(1)
    GPIO.output(5,GPIO.LOW)
    GPIO.output(6,GPIO.LOW)
    sleep(1)
GPIO.cleanup()