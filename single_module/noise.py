# 蜂鸣器

# 低电平触发

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)   #采用BCM编码
GPIO.setwarnings(False)

gpio_noise=17

GPIO.setup(gpio_noise,GPIO.OUT)

gpio_noise_frequency=100
gpio_noise_dc=1


p=GPIO.PWM(gpio_noise,gpio_noise_frequency)
p.start(gpio_noise_dc)

while(True):
    # for i in range(1, 10):     # 播放歌曲1
    #     p.ChangeFrequency(i) # 沿着歌曲的音符改变频率
    #     time.sleep(0.5)     # 一个节拍为0.5s的时长
     
    for i in range(1, 15):     # 播放歌曲1
        p.ChangeFrequency(i) # 沿着歌曲的音符改变频率
        time.sleep(0.5)     # 一个节拍为0.5s的时长

    # p.ChangeFrequency(1)
    # time.sleep(0.01)
    # p.ChangeFrequency(100)
    # time.sleep(0.01)

    # p.ChangeDutyCycle(100)
    # time.sleep(0.01)
    # p.ChangeDutyCycle(0)
    # time.sleep(0.01)

    # GPIO.output(gpio_noise,0)
    # time.sleep(0.01)
    # GPIO.output(gpio_noise,0)
    # time.sleep(0.01)


p.stop()
GPIO.cleanup()