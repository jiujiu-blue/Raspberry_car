# 小车发送超声波 并将接收端设为高电平  接收到超声波后，接收端变为低电平  
# 所以从发送到接收所经历的时间为高电平持续时间
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

#定义引脚
#STBY = 10

#左边两个轮子
PWMA = 18
AIN1 = 22
AIN2 = 27

#两个右边轮子
PWMB = 23
BIN1 = 25
BIN2 = 24

#红外循迹传感器GPIO
#Lred = 13
#Rred = 26
#超声波
trig=20#发射端
echo=21#接收端

#初始化
def init():
    #设置接触警告
    GPIO.setwarnings(False)
    #红外循迹传感器引脚初始化,设置为输入，接受红外信号
    #GPIO.setup(Lred,GPIO.IN)
    #GPIO.setup(Rred,GPIO.IN)
    #超声波
    GPIO.setup(trig,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(echo,GPIO.IN)
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
def turn_stop():
    L_Motor.ChangeDutyCycle(0) #设置占空比，控制速度
    GPIO.output(AIN1,0)
    GPIO.output(AIN2,0)
    R_Motor.ChangeDutyCycle(0) #设置占空比，控制速度
    GPIO.output(BIN1,0)
    GPIO.output(BIN2,0)
    #pwma.start(0)
    #pwmb.start(0)
    #time.sleep(0.1)

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
    turn_stop(speed,0.02)
    L_Motor.ChangeDutyCycle(speed) #设置占空比，控制速度
    GPIO.output(AIN2,0)
    GPIO.output(AIN1,0)
    R_Motor.ChangeDutyCycle(speed) #设置占空比，控制速度
    GPIO.output(BIN1,1)
    GPIO.output(BIN2,0)
    #pwma.start(speed)
    #pwmb.start(speed)
    time.sleep(t)


def turn_right(speed,t):
    turn_stop(speed,0.02)
    L_Motor.ChangeDutyCycle(speed) #设置占空比，控制速度
    GPIO.output(AIN1,1)
    GPIO.output(AIN2,0)
    R_Motor.ChangeDutyCycle(speed) #设置占空比，控制速度
    GPIO.output(BIN2,0)
    GPIO.output(BIN1,0)
    #pwma.start(speed)
    #pwmb.start(speed)
    time.sleep(t)
    

#红外循迹函数
def track():
    while True:
    	#接收两个红外传感器的信号
        LS=GPIO.input(Lred)
        RS=GPIO.input(Rred)
        #左右两个传感器都检测到黑色，小车在赛道上，前进
        if LS==True and RS==True:
            print("前进")
            turn_up(35,0.2)
        #左边的传感器没检测到黑色，说明小车车身偏离赛道靠左，右转将小车车身向右调整
        elif LS==False and RS==True:
            print("右转")
            turn_right(35,0.2)
        #右边的传感器没检测到黑色，说明小车车身偏离赛道靠右，左转将小车车身向左调整
        elif LS==True and RS==False:
            print("左转")
            turn_left(35,0.2)
        #两个传感器都没有检测到黑色，说明小车完全偏离赛道，停止
        else:
            print("停止")
            turn_stop()

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
    print("距离是：")			#返回距离
    print(distanceReturn)			#返回距离

def duoji():
    while True:
        disf=front_detection()
        if disf<40:
            turn_stop(0.2)
            turn_down(35,0.5)
            turn_stop(0.2)
            disl=left_detection()
            disr=right_detection()
            pwm.set_pwm(12, 0, 385)
            if disl<40 and disr<40:
                turn_left(35,1)
            elif disl>disr:
                turn_left(35,0.3)
                turn_stop(0.1)
            else :
                turn_right(35,0.3)
                turn_stop(0.1)
        else:
            turn_up(40,0)

#避障模块
#避障功能函数（超声波避障）
def bizhang():
    safe_dis=40 #设置一个安全距离
    while True:
        barrier_dis=Measure() #获取当前障碍物的距离
        print(barrier_dis,"cm")
        if (barrier_dis < safe_dis) == True:
            while (barrier_dis < safe_dis) == True:
                turn_down(30,0.3)
                barrier_dis=Measure() #获取当前障碍物的距离
                print(barrier_dis,"cm")
                turn_left(30,0.6)
                turn_up(25,0.5)
                turn_right(30,0.6)
            turn_right(34,1.2)
            #turn_right(30,0.5)
            turn_left(34,0.5)
        #turn_right(30,0.5)
        turn_up(25,0.4)
        time.sleep(0.6)
                

#主函数
if __name__=="__main__":
    init()
    L_Motor=GPIO.PWM(PWMA,100)
    L_Motor.start(0)
    R_Motor=GPIO.PWM(PWMB,100)
    R_Motor.start(0)
    try:
        while(True):
            print(Measure())
            time.sleep(1)
            # bizhang() #调用避障函数
    except KeyboardInterrupt:   #Ctrl+C 程序停止
        GPIO.cleanup()      #清除GPIO占用
