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
from MOVE import MOVE

class TRACK():

    #小车移动
    car_move=MOVE()

    #两个红外传感器
    gpio_redgre_1=13
    gpio_redgre_2=26    

    def __init__(self):
        GPIO.setup(self.gpio_redgre_1,GPIO.IN)
        GPIO.setup(self.gpio_redgre_2,GPIO.IN)

    def do_track(self):
        #接受循迹结果
        redgre_statu1=GPIO.input(self.gpio_redgre_1)
        redgre_statu2=GPIO.input(self.gpio_redgre_2)

        #根据循迹结果运行
        if(redgre_statu1==0 and redgre_statu2==0):#两边都是白线  直行
            self.car_move.turn_up(20,0.02)
            # print("都白 直行")
        elif(redgre_statu1==0 and redgre_statu2==1):#左边黑线右边白线  左转
            self.car_move.turn_stop(0.02)
            self.car_move.turn_left(30,0.02)
            # print("左转")
            # time.sleep(0.02)
        elif(redgre_statu1==1 and redgre_statu2==0):#左边白线右边黑线  右转
            self.car_move.turn_stop(0.02)
            # time.sleep(0.02)
            self.car_move.turn_right(30,0.02) 
            # time.sleep(0.02)
                
        elif(redgre_statu1==1 and redgre_statu2==1):#两边都是黑线  直行
            self.car_move.turn_up(20,0.02)
            # print("都黑 十字路口 直行")
            
    def end(self):
        self.car_move.turn_stop(0.1)

    def __del__(self):
        self.car_move.turn_stop(0.1)
        GPIO.cleanup()

    
    