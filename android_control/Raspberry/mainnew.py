"""
file: service.py
socket service
"""
 
 
import socket
import threading
import time
import sys
import re
import os
from MOVE import MOVE
from WAVE import WAVE
from LED import LED
from NOIZE import NOIZE
from cloud_move import cloud
from MAZE import MAZE
from TRACK import TRACK

speed=20
car_time=0.1
is_avoid=False
is_track=False

pic_num=0

#控制小车移动
def motorAction(command):
    global is_avoid
    global is_track
    if command=='ForwardZX':
        move.turn_up(speed,car_time)
    elif command=='BackZX':
        move.turn_down(speed,car_time)
    elif command=='LeftZX':
        move.turn_left(speed,car_time)
    elif command=='RightZX':
        move.turn_right(speed,car_time)
    elif command=='StopZX':
        move.turn_stop(car_time)
        is_avoid=False
        is_track=False
#控制舵机转向并测距
def angle_distance(command):
    if command[:command.index('Z')]=='turncsb':
        rel=r'Z(.*?)X'
        angle=re.findall(rel,command)
        angle=int(angle[0])
        wave.do_angle(angle)
    elif command=='csbmeasureZX':
        distance=wave.measure()
        print("距离是",distance)
#控制LED灯
def LED_control(command):
    if command[:command.index('Z')]=='led':
        rel=r'Z(.*?)X'
        ledwho=re.findall(rel,command)
        ledwho=int(ledwho[0])
        level=int(command.split('X')[1])
        led.do_led(ledwho,level)
        
#控制蜂鸣器
def noize_control(command):
    if command[:command.index('Z')]=='noise':
        rel=r'Z(.*?)X'
        frequency=re.findall(rel,command)
        frequency=int(frequency[0])
        t=float(command.split('X')[1])
        noize.do_noise(frequency,t)
#控制云台        
def cloud_control(command):
    if command=='cloudxieZX':
        cloud.front_below_detection()
    if command=='cloudfrontZX':
        cloud.left_below_detection()
    elif command=='cloudrightZX':
        cloud.right_below_detection()
    elif command=='cloudupZX':
        cloud.ab1_above_detection()
    elif command=='clouddownZX':
        cloud.ab3_above_detection()
    
def capture(command):
    global pic_num
    if command=='captureZX':
        pic_num+=1
        os.system('sudo killall -TERM motion')
        time.sleep(0.2)
        os.system('fswebcam --no-banner -r 1280x720 -S 10 /home/pi/Pictures/capture/image'+str(pic_num)+'.jpg')
        noize.do_noise(300,1)
        noize.do_noise(1,1)
        os.system('sudo 0.1')
        os.system('sudo motion')
        
#避障
def avoid(command):
    global is_avoid
    if command=='avoidZX':
        is_avoid=True

def avoidTRUE():
    while True:
        if is_avoid:
            while True:
                if not is_avoid:
                    maze.end()
                    break
                maze.avoiding()
 
#循迹
def track_in(command):
    global is_track
    if command=='trackZX':
        is_track=True

def trackTRUE():
    while True:
        if is_track:
            while True:
                if not is_track:
                    track.end()
                    break
                track.do_track()
        

def socket_service():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 防止socket server重启后端口被占用（socket.error: [Errno 98] Address already in use）
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', 6666))
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    except KeyboardInterrupt:
        exit(0) 
        
    print('Waiting connection...')
    
    #避障线程
    a=threading.Thread(target=avoidTRUE)
    a.start()
    
    #循迹线程
    T=threading.Thread(target=trackTRUE)
    T.start()  
 
    while 1:
        try:
            client, addr = s.accept()
            t = threading.Thread(target=deal_data, args=(client, addr))
            t.start()
        except socket.error:
            pass
        except KeyboardInterrupt:
           exit(0)
           
 
def deal_data(client, addr):
    print('Accept new connection from {0}'.format(addr))
    client.send(('Hi, Welcome to the server!').encode())
    while True:
        try:
            data=client.recv(1024)
            data=bytes.decode(data)
            if(len(data)==0):
                print('client {0} is closed'.format(addr))
                #oled.writeArea4(' Disconnect')
                break
            print("is receiving...")
            print(data)
            motorAction(data)
            angle_distance(data)  
            LED_control(data) 
            noize_control(data) 
            cloud_control(data)
            capture(data)
            avoid(data)
            track_in(data)
        except socket.error:
            continue
        except KeyboardInterrupt:
            client.close()
            exit(0)
 
if __name__ == '__main__':
    move=MOVE()
    wave=WAVE()
    led=LED()
    noize=NOIZE()
    maze=MAZE()
    track=TRACK()
    socket_service()
