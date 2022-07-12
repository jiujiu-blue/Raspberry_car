# 不不不不不不采用一直左转 直到检测到两条白线
# 小车循迹
# 白线 返回0  
# 黑线 返回1

# 问题一:检测不够灵敏
# 问题二:遇到黑线都灭后，灯又亮了

# 解决方案：
#1.调节滑动电阻，使其灵敏   √
#2.小车走慢点，转弯的时候也慢一点   √





import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)   #采用BCM编码
GPIO.setwarnings(False)

speed_const=15
speed_wheel1=20
speed_wheel2=20

# 两个左边轮子
gpio_wheel1_pwm=18
gpio_wheel1_in1=27
gpio_wheel1_in2=22

frequency_wheel1=100

GPIO.setup(gpio_wheel1_pwm,GPIO.OUT,initial=GPIO.LOW)   
GPIO.setup(gpio_wheel1_in1,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(gpio_wheel1_in2,GPIO.OUT,initial=GPIO.LOW)

pwm_wheel1=GPIO.PWM(gpio_wheel1_pwm,frequency_wheel1)
pwm_wheel1.start(speed_wheel1)

# 两个右边轮子
gpio_wheel2_pwm=23
gpio_wheel2_in1=24
gpio_wheel2_in2=25


frequency_wheel2=100

GPIO.setup(gpio_wheel2_pwm,GPIO.OUT,initial=GPIO.LOW)   
GPIO.setup(gpio_wheel2_in1,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(gpio_wheel2_in2,GPIO.OUT,initial=GPIO.LOW)

pwm_wheel2=GPIO.PWM(gpio_wheel2_pwm,frequency_wheel2)
pwm_wheel2.start(speed_wheel2)


#两个红外传感器
gpio_redgre_1=13
gpio_redgre_2=26    
GPIO.setup(gpio_redgre_1,GPIO.IN)
GPIO.setup(gpio_redgre_2,GPIO.IN)

    
def go_up():
    pwm_wheel1.ChangeDutyCycle(speed_const)
    pwm_wheel2.ChangeDutyCycle(speed_const)
    GPIO.output(gpio_wheel1_pwm,1)
    GPIO.output(gpio_wheel1_in1,0)
    GPIO.output(gpio_wheel1_in2,1)

    GPIO.output(gpio_wheel2_pwm,1)
    GPIO.output(gpio_wheel2_in1,0)
    GPIO.output(gpio_wheel2_in2,1)

        
def go_down():
    pwm_wheel1.ChangeDutyCycle(speed_const)
    pwm_wheel2.ChangeDutyCycle(speed_const)
    GPIO.output(gpio_wheel1_pwm,1)
    GPIO.output(gpio_wheel1_in1,1)
    GPIO.output(gpio_wheel1_in2,0)

    GPIO.output(gpio_wheel2_pwm,1)
    GPIO.output(gpio_wheel2_in1,1)
    GPIO.output(gpio_wheel2_in2,0)
    

def go_left():
    # speed_wheel1=20
    # speed_wheel2=40
    # pwm_wheel1.ChangeDutyCycle(speed_wheel1)
    # pwm_wheel2.ChangeDutyCycle(speed_wheel2)
    GPIO.output(gpio_wheel1_pwm,1)
    GPIO.output(gpio_wheel1_in1,1)
    GPIO.output(gpio_wheel1_in2,0)

    GPIO.output(gpio_wheel2_pwm,1)
    GPIO.output(gpio_wheel2_in1,0)
    GPIO.output(gpio_wheel2_in2,1)


def go_right():
    # speed_wheel1=20
    # speed_wheel2=40
    # pwm_wheel1.ChangeDutyCycle(speed_wheel1)
    # pwm_wheel2.ChangeDutyCycle(speed_wheel2)
    GPIO.output(gpio_wheel1_pwm,1)
    GPIO.output(gpio_wheel1_in1,0)
    GPIO.output(gpio_wheel1_in2,1)

    GPIO.output(gpio_wheel2_pwm,1)
    GPIO.output(gpio_wheel2_in1,1)
    GPIO.output(gpio_wheel2_in2,0)

def go_stop():
    GPIO.output(gpio_wheel1_pwm,0)
    GPIO.output(gpio_wheel1_in1,0)
    GPIO.output(gpio_wheel1_in2,0)

    GPIO.output(gpio_wheel2_pwm,0)
    GPIO.output(gpio_wheel2_in1,0)
    GPIO.output(gpio_wheel2_in2,0)



def destory():
    GPIO.cleanup()
    pwm_wheel1.stop()
    pwm_wheel2.stop()



if __name__ == '__main__':      # 程序从这里开始
    # 白线 返回0  
    # 黑线 返回1
    while(True):
        #接受循迹结果
        redgre_statu1=GPIO.input(gpio_redgre_1)
        redgre_statu2=GPIO.input(gpio_redgre_2)

        #根据循迹结果运行
        if(redgre_statu1==0 and redgre_statu2==0):#两边都是白线  直行
            go_up()
            print("都白 直行")
        elif(redgre_statu1==0 and redgre_statu2==1):#左边黑线右边白线  左转
            go_stop()
            time.sleep(0.02)
            go_left()
            print("左转")
            time.sleep(0.02)
        elif(redgre_statu1==1 and redgre_statu2==0):#左边白线右边黑线  右转
            go_stop()
            time.sleep(0.02)
            go_right() 
            time.sleep(0.02)
            
        elif(redgre_statu1==1 and redgre_statu2==1):#两边都是黑线  直行
            go_up()
            print("都黑 十字路口 直行")
        time.sleep(0.1)
    
    destory()
    # while(True):
    #     statu1=GPIO.input(gpio_redgre_1)
    #     print(statu1)
    #     time.sleep(0.5)
    #     # statu2=GPIO.

    # go_left()
    # time.sleep(1)
    # destory()

    # return 

    # #先快跑 再慢跑
    # go_up()
    # time.sleep(1)
    # speed_wheel1=10
    # speed_wheel2=10
    # pwm_wheel1.ChangeDutyCycle(speed_wheel1)
    # pwm_wheel2.ChangeDutyCycle(speed_wheel2)
    # time.sleep(2)
    
    # destory()
    
    