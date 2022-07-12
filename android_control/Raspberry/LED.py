# 绿灯开关  按一次，绿灯常亮。再按一次，绿灯熄灭

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)   #采用BCM编码
GPIO.setwarnings(False)

class LED:

    gpio_led_red=5
    gpio_led_green=6

    # gpio_control_led=19

    def __init__(self):
        GPIO.setup(self.gpio_led_red,GPIO.OUT)
        GPIO.setup(self.gpio_led_green,GPIO.OUT)   

        # GPIO.setup(gpio_control_led,GPIO.IN)

    def do_led(self,gpio_led,level):
        GPIO.output(gpio_led,level)

    def __del__(self):
        GPIO.cleanup()  