import RPi.GPIO as GPIO
import time
import sys
import Adafruit_PCA9685 
from cloud_move import cloud

GPIO.setmode(GPIO.BCM)

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)

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
                cloud.front_below_detection()
            elif choice == '2':
                cloud.right_below_detection()
            elif choice == '3':
                cloud.left_below_detection()
            elif choice == '4':
                cloud.ab1_above_detection()
            elif choice == '5':
                cloud.ab2_above_detection()
            elif choice == '6':
                cloud.ab3_above_detection()
            else: 
                break
    except KeyboardInterrupt:
        GPIO.cleanup()
        fp.close()