# 蜂鸣器

# 低电平触发

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)   #采用BCM编码
GPIO.setwarnings(False)

class NOIZE:
        
    gpio_noise=17
    # gpio_noise_frequency=100
    # gpio_noise_dc=1

    GPIO.setup(gpio_noise,GPIO.OUT,initial=GPIO.LOW)
    p=GPIO.PWM(gpio_noise,1)
    p.start(1)

    def __init__(self):
        GPIO.setup(self.gpio_noise,GPIO.OUT,initial=GPIO.LOW)

    def do_noise(self,frequency,time_noise):
        self.p.ChangeFrequency(frequency) # 沿着歌曲的音符改变频率
        time.sleep(time_noise)     # 一个节拍为0.5s的时长

    def __del__(self):
        GPIO.cleanup()
        self.p.stop()
        
