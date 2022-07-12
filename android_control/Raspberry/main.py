"""
file: service.py
socket service
"""
 
 
import socket
import threading
import time
import sys
import os
import signal
from MOVE import MOVE

speed=20
time=0.02


def motorAction(command):
    if command=='Forward':
        move.turn_up(speed,time)
    elif command=='Back':
        move.turn_down(speed,time)
    elif command=='Left':
        move.turn_left(speed,time)
    elif command=='Right':
        move.turn_right(speed,time)
    elif command=='Stop':
       move.turn_stop(time)
'''
def test(command):
    while(test!=stop)
'''
def esc(command,pid):
    if command=='esc':
        os.kill(pid, signal.SIGKILL)  # kill子进程
        print('avoiding obstacle is done')
        return True
    else:
        return False
        

def avoid(client,addr,command):
    if command=='avoid':
        pid=os.fork()
        if pid ==0:
            while True:
                print("I'am child")   
            print(os.getpid())
        else:
            while True:
                try:
                    data=client.recv(1024)
                    data=bytes.decode(data)
                    if(len(data)==0):
                        print('client {0} is closed'.format(addr))
                        #oled.writeArea4(' Disconnect')
                        break
                    if esc(data,pid): 
                        break                     
                except socket.error:
                    continue
                except KeyboardInterrupt:
                    break
            deal_data(client, addr)
    
    
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
    print('Waiting connection...')
 
    while 1:
        try:
            client, addr = s.accept()
            t = threading.Thread(target=deal_data, args=(client, addr))
            t.start()
        except socket.error:
            pass
        except KeyboardInterrupt:
            move.destroy()
 
def deal_data(client, addr):
    print('Accept new connection from {0}'.format(addr))
    client.send(('Hi, Welcome to the server!').encode())
    print('hahhah')
    print(os.getpid())
    while True:
        #cameraAction(steer,cameraActionState)
        try:
            data=client.recv(1024)
            data=bytes.decode(data)
            if(len(data)==0):
                print('client {0} is closed'.format(addr))
                #oled.writeArea4(' Disconnect')
                break
            motorAction(data)
            avoid(client,addr,data)              
            #motorAction(motor,data)
            #cameraActionState=setCameraAction(data)
        except socket.error:
            continue
        except KeyboardInterrupt:
            client.close()
            break
 
if __name__ == '__main__':
    move=MOVE()
    socket_service()