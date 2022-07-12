import RPi.GPIO as GPIO
import time
import sys
import Adafruit_PCA9685             # 调用PCA9685模块

class WAVE:
    # #舵机转动角度
    # duoji_angle_front=390
    # duoji_angle_left=750
    # duoji_angle_right=150

    #超声波
    trig=20#发射端
    echo=21#接收端
    pwm = Adafruit_PCA9685.PCA9685()
    pwm.set_pwm_freq(60)

    #初始化
    def __init__(self):
        #超声波
        GPIO.setup(self.trig,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.echo,GPIO.IN)

    def do_angle(self,angle):
        self.pwm.set_pwm(12, 0, angle)
        time.sleep(1)

    #超声波测距
    def measure(self):
        #超声波测距函数
        GPIO.output(self.trig,GPIO.LOW)		#输出口初始化置LOW（不发射）
        time.sleep(0.000002)
        GPIO.output(self.trig,GPIO.HIGH)		#发射超声波
        time.sleep(0.00001)
        GPIO.output(self.trig,GPIO.LOW)		#停止发射超声波
        while GPIO.input(self.echo) == 0:
            emitTime = time.time()		#记录发射时间
        while GPIO.input(self.echo) == 1:
            acceptTime = time.time()	#记录接收时间
        totalTime = acceptTime - emitTime		#计算总时间
        distanceReturn = totalTime * 340 / 2 * 100  	#计算距离（单位：cm）
        return distanceReturn

    def __del__(self):
        GPIO.cleanup()
