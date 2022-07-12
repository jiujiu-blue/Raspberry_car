import RPi.GPIO as GPIO 
import time
GPIO.setmode(GPIO.BCM)
TRIG=20
ECHO=21
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
#超声波测距函数
GPIO.output(TRIG,GPIO.LOW)		#输出口初始化置LOW（不发射）
time.sleep(0.000002)
GPIO.output(TRIG,GPIO.HIGH)		#发射超声波
time.sleep(0.00001)
GPIO.output(TRIG,GPIO.LOW)		#停止发射超声波
while GPIO.input(ECHO) == 0:
    emitTime = time.time()		#记录发射时间
while GPIO.input(ECHO) == 1:
    acceptTime = time.time()	#记录接收时间
totalTime = acceptTime - emitTime		#计算总时间
distanceReturn = totalTime * 340 / 2 * 100  	#计算距离（单位：cm）
print("距离是：")			#返回距离
print(distanceReturn)			#返回距离

