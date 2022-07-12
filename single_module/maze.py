import RPi.GPIO as GPIO
import time
import sys
import Adafruit_PCA9685             # 调用PCA9685模块

GPIO.setmode(GPIO.BCM)

#安全距离
safe_dis=15

#舵机转动角度
duoji_angle_front=390
duoji_angle_left=750
duoji_angle_right=150

#输出到日志

fp = open("/home/pi/code/car/log.txt", "w+")  
# w+打开一个文件用于读写。
#如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。


#定义引脚

#左边两个轮子
PWMA = 18
AIN1 = 22
AIN2 = 27

#两个右边轮子
PWMB = 23
BIN1 = 25
BIN2 = 24

#红外循迹/避障传感器GPIO
L_red = 12
R_red = 16
#超声波
trig=20#发射端
echo=21#接收端
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)
#初始化
def init():
    #设置接触警告
    GPIO.setwarnings(False)
    #红外循迹传感器引脚初始化,设置为输入，接受红外信号
    GPIO.setup(L_red,GPIO.IN)
    GPIO.setup(R_red,GPIO.IN)
    #超声波
    GPIO.setup(trig,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(echo,GPIO.IN)
    #舵机
    #设置 GPIO 的工作方式
    #GPIO.setup(STBY, GPIO.OUT)
    GPIO.setup(PWMA, GPIO.OUT)
    GPIO.setup(AIN1, GPIO.OUT)
    GPIO.setup(AIN2, GPIO.OUT)
    GPIO.setup(PWMB, GPIO.OUT)
    GPIO.setup(BIN1, GPIO.OUT)
    GPIO.setup(BIN2, GPIO.OUT)
    #pwma = GPIO.PWM(PWMA,100)#控制小车速度，初始设置
    #pwmb = GPIO.PWM(PWMB,100)

#基础行为方向
def turn_up(speed,t):
    L_Motor.ChangeDutyCycle(speed) #设置占空比，控制速度
    GPIO.output(AIN1,1)
    GPIO.output(AIN2,0)
    R_Motor.ChangeDutyCycle(speed) #设置占空比，控制速度
    GPIO.output(BIN1,1)
    GPIO.output(BIN2,0)
    #pwma.start(speed)
    #pwmb.start(speed)
    time.sleep(t)


def turn_down(speed,t):
    L_Motor.ChangeDutyCycle(speed) #设置占空比，控制速度
    GPIO.output(AIN2,1)
    GPIO.output(AIN1,0)
    R_Motor.ChangeDutyCycle(speed) #设置占空比，控制速度
    GPIO.output(BIN2,1)
    GPIO.output(BIN1,0)
    #pwma.start(speed)
    #pwmb.start(speed)
    time.sleep(t)


def turn_left(speed,t):
    turn_stop(0.02)
    L_Motor.ChangeDutyCycle(speed) #设置占空比，控制速度
    GPIO.output(AIN2,1)
    GPIO.output(AIN1,0)
    R_Motor.ChangeDutyCycle(speed) #设置占空比，控制速度
    GPIO.output(BIN1,1)
    GPIO.output(BIN2,0)
    #pwma.start(speed)
    #pwmb.start(speed)
    time.sleep(t)


def turn_right(speed,t):
    turn_stop(0.02)
    L_Motor.ChangeDutyCycle(speed) #设置占空比，控制速度
    GPIO.output(AIN1,1)
    GPIO.output(AIN2,0)
    R_Motor.ChangeDutyCycle(speed) #设置占空比，控制速度
    GPIO.output(BIN2,1)
    GPIO.output(BIN1,0)
    #pwma.start(speed)
    #pwmb.start(speed)
    time.sleep(t)
    
def turn_stop(t):
    L_Motor.ChangeDutyCycle(0) #设置占空比，控制速度
    GPIO.output(AIN1,0)
    GPIO.output(AIN2,0)
    R_Motor.ChangeDutyCycle(0) #设置占空比，控制速度
    GPIO.output(BIN1,0)
    GPIO.output(BIN2,0)
    #pwma.start(0)
    #pwmb.start(0)
    time.sleep(t)


#超声波测距
def Measure():
    #超声波测距函数
    GPIO.output(trig,GPIO.LOW)		#输出口初始化置LOW（不发射）
    time.sleep(0.000002)
    GPIO.output(trig,GPIO.HIGH)		#发射超声波
    time.sleep(0.00001)
    GPIO.output(trig,GPIO.LOW)		#停止发射超声波
    while GPIO.input(echo) == 0:
        emitTime = time.time()		#记录发射时间
    while GPIO.input(echo) == 1:
        acceptTime = time.time()	#记录接收时间
    totalTime = acceptTime - emitTime		#计算总时间
    distanceReturn = totalTime * 340 / 2 * 100  	#计算距离（单位：cm）
    # print("距离是：")			#返回距离
    # print(distanceReturn)			#返回距离
    return distanceReturn


#红外避障函数
def redbizhang():
    # while True:
    L_s=GPIO.input(L_red)
    R_s=GPIO.input(R_red)
    if L_s == False and R_s ==True: #左边有障碍物
        print("边距过小 右偏",file=fp)
        print("边距过小 右偏")
        #turn_down(30,0)
        turn_right(50,0.1)
        #turn_up(20,0)
    elif L_s==True and R_s ==False:  #右边有障碍物
        print("边距过小 左偏",file=fp)
        print("边距过小 左偏")
        #turn_down(30,0)
        turn_left(50,0.1)
        #turn_up(20,0)
    # else: #前方有障碍物或者两边都有障碍物
    #     turn_stop(0.2)
    #     turn_down(20,0.3)
    #     turn_left(25,0.4)
    #     #turn_right(20,0.3)
    #     #turn_up(20,0.3)

#超声波方向避障
def front_detection():
    pwm.set_pwm(12, 0, duoji_angle_front)
    time.sleep(1)
    dis_f=Measure()
    return dis_f

def left_detection():
    pwm.set_pwm(12, 0, duoji_angle_left)
    time.sleep(1)
    dis_l=Measure()
    return dis_l

def right_detection():
    pwm.set_pwm(12, 0,duoji_angle_right)
    time.sleep(1)
    dis_r=Measure()
    return dis_r


#避障模块
#超声波舵机避障
def duoji():
    pwm.set_pwm(12, 0, 390)
    time.sleep(1)
    cnt_block=0
    while True:
        redbizhang()#保持边距
        disf=Measure()
        # print("disf为",disf)
        if disf<safe_dis:
            print("前方障碍物 不能直行",file=fp)
            print("前方障碍物 不能直行")
            turn_stop(0.2)
            # turn_down(35,0.5)
            # turn_stop(0.2)
            disr=right_detection()
            disl=left_detection()
            cnt_block=cnt_block+1
            
            print("距离左边距离",disl)
            print("距离右边距离",disr)
            pwm.set_pwm(12, 0, 370)
            time.sleep(1)
            if disl>disr:
            # if cnt_block==1:
                # print("第一次遇到障碍物 左转")
                print("左边出口大 左转",file=fp)
                print("左边出口大 左转")
                turn_left(100,0.1)
                turn_stop(0.1)
            elif disl<disr:
            # elif (cnt_block>=2 and cnt_block<=3):
                # print("第二或三次遇到障碍物 右转")
                print("右边出口大 右转",file=fp)
                print("右边出口大 右转")
                turn_right(100,0.1)
                turn_stop(0.1)
            # elif (cnt_block>=4):
            #     print("第四次遇到障碍物 左转")
            #     # print("右边出口大 右转",file=fp)
            #     # print("右边出口大 右转")
            #     turn_left(100,0.3)
            #     turn_stop(0.1)
            
        else:
            turn_up(20,0.05)

                


#主函数
if __name__=="__main__":
    init()
    L_Motor=GPIO.PWM(PWMA,100)
    L_Motor.start(0)
    R_Motor=GPIO.PWM(PWMB,100)
    R_Motor.start(0)
    # turn_left(50,0.1)
    # turn_stop(1)
    # time.sleep(10)
    # while(True):
    #     dis=right_detection()
    #     print("距离右边距离",dis)
    #     time.sleep(1)
    # front_detection()
    # left_detection()
    # right_detection()
    # time.sleep(10)
    # turn_left(100,0.1)
    # turn_stop(10)
    try:
        # while(True):
        #     print("距离右边距离为 ",right_detection())
        front_detection()
        duoji()
        # front_detection()
        # # print("我打fsda", file=fp)
        # while(True):
        #     print(Measure())
        #     time.sleep(1)
        #     # bizhang() #调用避障函数
    except KeyboardInterrupt:   #Ctrl+C 程序停止
        GPIO.cleanup()      #清除GPIO占用
        fp.close()
        # pwm.set_pwm_freq(0)
