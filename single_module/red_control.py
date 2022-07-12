import RPi.GPIO as GPIO
import time
import sys
import lirc

GPIO.setmode(GPIO.BCM)

#定义引脚
#STBY = 10
PWMA = 18
PWMB = 23
AIN1 = 22
AIN2 = 27
BIN1 = 25
BIN2 = 24
#红外循迹/避障传感器GPIO
L_red = 12
R_red = 16
#超声波
trig=20#发射端
echo=21#接收端
#红外遥控
#sockid=lirc.init("irexec","lircrc",blocking=False)

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
            turn_stop(0.2)

#超声波测距
def Measure():
    GPIO.output(trig,GPIO.HIGH) #给Trig发送高电平，发出触发信号
    time.sleep(0.00015) #需要至少10us的高电平信号，触发Trig测距
    GPIO.output(trig,GPIO.LOW)
    while GPIO.input(echo)!=GPIO.HIGH: #等待接收高电平
        pass
    t1=time.time() #记录信号发出的时间
    while GPIO.input(echo)==GPIO.HIGH: #接收端还没接收到信号变成低电平就循环等待（等高电平结束）
        pass
    t2=time.time() #记录接收到反馈信号的时间
    distance=(t2-t1)*340*100/2 #计算距离，单位换成cm
    return distance

#避障模块
#避障功能函数（超声波避障）
def csbbizhang():
    safe_dis=40 #设置一个安全距离
    while True:
        barrier_dis=Measure() #获取当前障碍物的距离
        print(barrier_dis,"cm")
        if (barrier_dis < safe_dis) == True:
            while (barrier_dis < safe_dis) == True:
                turn_down(25,0.3)
                barrier_dis=Measure() #获取当前障碍物的距离
                print(barrier_dis,"cm")
                #redbizhang()
                turn_left(30,0.6)
                turn_up(25,0.5)
                turn_right(30,0.6)
            turn_right(35,1.2)
            #turn_right(30,0.5)
            turn_left(30,0.5)
        #turn_right(30,0.5)
        turn_up(25,0.4)
        time.sleep(0.6)
                
#红外避障函数
def redbizhang():
        L_s=GPIO.input(L_red)
        R_s=GPIO.input(R_red)
        if L_s == True and R_s == True: # 高电平表示无障碍
            print("turn_up")
            turn_up(20,0)
        elif L_s == True and R_s ==False: #右边有障碍物
            print("Left")
            #turn_down(30,0)
            turn_left(35,0)
            #turn_up(20,0)
        elif L_s==False and R_s ==True:  #左边有障碍物
            print("Right")
            #turn_down(30,0)
            turn_right(35,0)
            #turn_up(20,0)
        else: #前方有障碍物或者两边都有障碍物
            turn_stop(0.2)
            turn_down(20,0.3)
            turn_left(25,0.4)
            #turn_right(20,0.3)
            #turn_up(20,0.3)

#红外遥控函数,速度越快越灵敏
def red_control(data):#解析按键
    #while True:
        #code_ir=lirc.nextcode()
        
        if data=='echo "RIGHT"':
            print("右拐")
            turn_right(60,0)
            time.sleep(0.1)
        elif data=='echo "LEFT"':
            print("左拐")
            turn_left(60,0)
            time.sleep(0.1)
        elif data=='echo "STOP"':
            print("停止")
            turn_stop(0)
            time.sleep(0.1)
        elif data=='echo "UP"':
            print("前进")
            turn_up(60,0)
            time.sleep(0.1)
        elif data=='echo "DOWN"':
            print("后退")
            turn_down(60,0)
            time.sleep(0.1)
def remote():
    with lirc.LircdConnection("irexec",) as conn:
            while True:
                string = conn.readline()
                red_control(string)

#主函数
if __name__=="__main__":
    init()
    L_Motor=GPIO.PWM(PWMA,100)
    L_Motor.start(0)
    R_Motor=GPIO.PWM(PWMB,100)
    R_Motor.start(0)
    try:
        #bizhang() #调用避障函数
        remote()
    except KeyboardInterrupt:   #Ctrl+C 程序停止
        #lirc.deinit()
        GPIO.cleanup()      #清除GPIO占用
