import RPi.GPIO as GPIO
import time
import sys
import Adafruit_PCA9685             # 调用PCA9685模块
from MOVE import MOVE

class MAZE:
    car_move=MOVE()
    #安全距离
    safe_dis=15

    #舵机转动角度
    duoji_angle_front=390
    duoji_angle_left=750
    duoji_angle_right=150

    #红外循迹/避障传感器GPIO
    L_red = 12
    R_red = 16

    #超声波
    trig=20#发射端
    echo=21#接收端
    pwm = Adafruit_PCA9685.PCA9685()
    pwm.set_pwm_freq(60)

    #初始化
    def __init__(self):
        #红外循迹传感器引脚初始化,设置为输入，接受红外信号
        GPIO.setup(self.L_red,GPIO.IN)
        GPIO.setup(self.R_red,GPIO.IN)
        #超声波
        GPIO.setup(self.trig,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.echo,GPIO.IN)

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
        print(distanceReturn)
        return distanceReturn


    #红外避障函数
    def redbizhang(self):
        print('red bizhang')
        # while True:
        L_s=GPIO.input(self.L_red)
        R_s=GPIO.input(self.R_red)
        if L_s == False and R_s ==True: #左边有障碍物
            # print("边距过小 右偏",file=fp)
            print("边距过小 右偏")
            self.car_move.turn_right(50,0.1)
        elif L_s==True and R_s ==False:  #右边有障碍物
            # print("边距过小 左偏",file=fp)
            print("边距过小 左偏")
            self.car_move.turn_left(50,0.1)

    #超声波方向避障
    def front_detection(self):
        print('front detection')
        self.pwm.set_pwm(12, 0, self.duoji_angle_front)
        time.sleep(1)
        dis_f=self.measure()
        return dis_f

    def left_detection(self):
        self.pwm.set_pwm(12, 0, self.duoji_angle_left)
        time.sleep(1)
        dis_l=self.measure()
        return dis_l

    def right_detection(self):
        self.pwm.set_pwm(12, 0,self.duoji_angle_right)
        time.sleep(1)
        dis_r=self.measure()
        return dis_r
    #检测
    def detect(self):
        self.front_detection()
        self.pwm.set_pwm(12, 0, 390)
        time.sleep(1)
        print("bizhang") 
    
    #避障
    def avoiding(self):
        print('bizhang---------')
        self.redbizhang()#保持边距
        disf=self.measure()
        if disf<self.safe_dis:
            print('if循环')
            # print("前方障碍物 不能直行",file=fp)
            print("前方障碍物 不能直行")
            self.car_move.turn_stop(0.2)
            disr=self.right_detection()
            disl=self.left_detection()
                
            print("距离左边距离",disl)
            print("距离右边距离",disr)
            self.pwm.set_pwm(12, 0, 370)
            time.sleep(1)
            if disl>disr:
                print("左边出口大 左转")
                self.car_move.turn_left(100,0.1)
                self.car_move.turn_stop(0.1)
            elif disl<disr:
                print("右边出口大 右转")
                self.car_move.turn_right(100,0.1)
                self.car_move.turn_stop(0.1)
                
        else:
            print('直行')
            self.car_move.turn_up(20,0.05)   
        
    def end(self):
        self.car_move.turn_stop(0.1)     

    def __del__(self):
        GPIO.cleanup()
