# 绿灯开关  按一次，绿灯常亮。再按一次，绿灯熄灭

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)   #采用BCM编码
GPIO.setwarnings(False)

# gpio_led_1=5
gpio_led_2=6

gpio_control_led=19

GPIO.setup(gpio_led_2,GPIO.OUT)   #指定使用4号编口

GPIO.setup(gpio_control_led,GPIO.IN)

# statu_1=0
flag=0
while(True):
    ff=1-flag
    while(GPIO.input(gpio_control_led)==1):
        flag=ff

    # if(statu_2!=statu_1):
    #     statu_1=statu_2
    #     flag=1-flag
    
    # print(statu_2)
    GPIO.output(gpio_led_2,flag)
    # time.sleep(1)

    # time.sleep(1)
    # GPIO.output(gpio_led_2,GPIO.LOW)
    # time.sleep(1)

GPIO.cleanup()