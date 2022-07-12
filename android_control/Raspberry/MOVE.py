import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
class MOVE:
    #定义引脚

    #左边两个轮子
    gpio_wheel1_pwm = 18
    gpio_wheel1_in1 = 22
    gpio_wheel1_in2 = 27

    #两个右边轮子
    gpio_wheel2_pwm = 23
    gpio_wheel2_in1 = 25
    gpio_wheel2_in2 = 24    
    
    #两个电机
    GPIO.setup(gpio_wheel1_pwm, GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(gpio_wheel2_pwm, GPIO.OUT,initial=GPIO.LOW)
    motor_left=GPIO.PWM(gpio_wheel1_pwm,100)
    motor_right=GPIO.PWM(gpio_wheel2_pwm,100)
    motor_left.start(0)
    motor_right.start(0)

    
    def __init__(self):
        print("gouzao")
        GPIO.setup(self.gpio_wheel1_pwm, GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.gpio_wheel1_in1, GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.gpio_wheel1_in2, GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.gpio_wheel2_pwm, GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.gpio_wheel2_in1, GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.gpio_wheel2_in2, GPIO.OUT,initial=GPIO.LOW)
        
    #基础行为方向
    def turn_up(self,speed,t):
        print("turn_up")
        print(speed)
        self.motor_left.ChangeDutyCycle(speed) #设置占空比，控制速度
        GPIO.output(self.gpio_wheel1_in1,1)
        GPIO.output(self.gpio_wheel1_in2,0)
        self.motor_right.ChangeDutyCycle(speed) #设置占空比，控制速度
        GPIO.output(self.gpio_wheel2_in1,1)
        GPIO.output(self.gpio_wheel2_in2,0)
        time.sleep(t)


    def turn_down(self,speed,t):
        self.motor_left.ChangeDutyCycle(speed) #设置占空比，控制速度
        GPIO.output(self.gpio_wheel1_in2,1)
        GPIO.output(self.gpio_wheel1_in1,0)
        self.motor_right.ChangeDutyCycle(speed) #设置占空比，控制速度
        GPIO.output(self.gpio_wheel2_in2,1)
        GPIO.output(self.gpio_wheel2_in1,0)
        time.sleep(t)


    def turn_left(self,speed,t):
        self.turn_stop(0.02)
        self.motor_left.ChangeDutyCycle(speed) #设置占空比，控制速度
        GPIO.output(self.gpio_wheel1_in2,1)
        GPIO.output(self.gpio_wheel1_in1,0)
        self.motor_right.ChangeDutyCycle(speed) #设置占空比，控制速度
        GPIO.output(self.gpio_wheel2_in1,1)
        GPIO.output(self.gpio_wheel2_in2,0)
        time.sleep(t)


    def turn_right(self,speed,t):
        self.turn_stop(0.02)
        self.motor_left.ChangeDutyCycle(speed) #设置占空比，控制速度
        GPIO.output(self.gpio_wheel1_in1,1)
        GPIO.output(self.gpio_wheel1_in2,0)
        self.motor_right.ChangeDutyCycle(speed) #设置占空比，控制速度
        GPIO.output(self.gpio_wheel2_in2,1)
        GPIO.output(self.gpio_wheel2_in1,0)
        time.sleep(t)
        
    def turn_stop(self,t):
        self.motor_left.ChangeDutyCycle(0) #设置占空比，控制速度
        GPIO.output(self.gpio_wheel1_in1,0)
        GPIO.output(self.gpio_wheel1_in2,0)
        self.motor_right.ChangeDutyCycle(0) #设置占空比，控制速度
        GPIO.output(self.gpio_wheel2_in1,0)
        GPIO.output(self.gpio_wheel2_in2,0)
        time.sleep(t)
    def end(self):
        GPIO.cleanup()
        self.moter_left.stop()
        self.moter_right.stop()

    def __del__(self):
        GPIO.cleanup()      #清除GPIO占用
        self.motor_left.stop()
        self.motor_right.stop()
   
