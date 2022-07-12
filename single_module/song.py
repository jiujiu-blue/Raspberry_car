

import RPi.GPIO as GPIO
import time

Buzzer = 17

CL = [0, 131, 147, 165, 175, 196, 211, 248]     # 低音C调音符对应的频率

CM = [0, 262, 294, 330, 350, 393, 441, 495]     # 中音C调音符对应的频率

CH = [0, 525, 589, 661, 700, 786, 882, 990]     # 高音C调音符对应的频率

song_1 = [  CM[3], CM[5], CM[6], CM[3], CM[2], CM[3], CM[5], CM[6], # 歌曲1的音符
            CH[1], CM[6], CM[5], CM[1], CM[3], CM[2], CM[2], CM[3], 
            CM[5], CM[2], CM[3], CM[3], CL[6], CL[6], CL[6], CM[1],
            CM[2], CM[3], CM[2], CL[7], CL[6], CM[1], CL[5] ]

beat_1 = [  1, 1, 3, 1, 1, 3, 1, 1,             # 歌曲1的节拍, 1 指 1/8 拍
            1, 1, 1, 1, 1, 1, 3, 1, 
            1, 3, 1, 1, 1, 1, 1, 1, 
            1, 2, 1, 1, 1, 1, 1, 1, 
            1, 1, 3 ]

song_2 = [  CM[1], CM[1], CM[1], CL[5], CM[3], CM[3], CM[3], CM[1], # 歌曲2的音符
            CM[1], CM[3], CM[5], CM[5], CM[4], CM[3], CM[2], CM[2], 
            CM[3], CM[4], CM[4], CM[3], CM[2], CM[3], CM[1], CM[1], 
            CM[3], CM[2], CL[5], CL[7], CM[2], CM[1]    ]

beat_2 = [  1, 1, 2, 2, 1, 1, 2, 2,             # 歌曲2的节拍, 1 指 1/8 拍
            1, 1, 2, 2, 1, 1, 3, 1, 
            1, 2, 2, 1, 1, 2, 2, 1, 
            1, 2, 2, 1, 1, 3 ]

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)        # 根据物理位置对gpio进行编号
    GPIO.setup(Buzzer, GPIO.OUT)    # 设置引脚模式为输出
    global Buzz                     # 指定一个全局变量来替换GPIO.PWM
    Buzz = GPIO.PWM(Buzzer, 440)    # 440 是初始频率
    Buzz.start(50)                  # 启动蜂鸣器PWM50%的占空比

def loop():
    while True:
        print('\n    Playing song 1...')
        for i in range(1, len(song_1)):     # 播放歌曲1
            Buzz.ChangeFrequency(song_1[i]) # 沿着歌曲的音符改变频率
            time.sleep(beat_1[i] * 0.5)     # 一个节拍为0.5s的时长
        time.sleep(1)                       # 

        print('\n\n    Playing song 2...')
        for i in range(1, len(song_2)):     
            Buzz.ChangeFrequency(song_2[i]) 
            time.sleep(beat_2[i] * 0.5)     

def destory():
    Buzz.stop()                 # 停止PWM
    GPIO.output(Buzzer, 1)      # 将蜂鸣器引脚设置为输出高电平
    GPIO.cleanup()              # 释放资源

if __name__ == '__main__':      # 程序从这里开始
    setup()
    try:
        loop()
    except KeyboardInterrupt:   # 当输入'Ctrl+C'时, 函数destroy()会被执行
        destory()