import RPi.GPIO as GPIO
import time
import sys
import Adafruit_PCA9685 

GPIO.setmode(GPIO.BCM)

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(20)

class cloud:
    def front_below_detection():
        pwm.set_pwm(13, 0, 350)
        time.sleep(1)

    def left_below_detection():
        pwm.set_pwm(13, 0, 650)
        time.sleep(1)

    def right_below_detection():
        pwm.set_pwm(13, 0, 100)
        time.sleep(1)

    def ab1_above_detection():
        pwm.set_pwm(14, 0, 60)
        time.sleep(1)

    def ab2_above_detection():
        pwm.set_pwm(14, 0, 180)
        time.sleep(1)

    def ab3_above_detection():
        pwm.set_pwm(14, 0, 350)
        time.sleep(1)

#主函数
'''
if __name__=="__main__":
    try:
        #front_below_detection()
        #right_below_detection()
        #left_below_detection()
        #ab1_above_detection()
        #ab2_above_detection()
        #ab3_above_detection()
        #cloud()
        while True:
            choice = input('输入：')
            if choice == '1':
                front_below_detection()
            elif choice == '2':
                    right_below_detection()
            elif choice == '3':
                left_below_detection()
            elif choice == '4':
                ab1_above_detection()
            elif choice == '5':
                ab2_above_detection()
            elif choice == '6':
                ab3_above_detection()
            else: 
                break
    except KeyboardInterrupt:
        GPIO.cleanup()
        fp.close()
'''
