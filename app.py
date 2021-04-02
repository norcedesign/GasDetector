import sys
import time
import socket
import threading
#import datetime
import concurrent.futures
import service

from array import *
#from threading import Semaphore, Thread

HOST: str = '192.168.1.107'  # update to the desired ip address
PORT1: int = 1231  # update to the desired port
PORT2: int = 1232  # update to the desired port

threadLock = threading.Lock()
#sem = threading.Semaphore()

gaslevel = array('B', [0, 0, 0])

def parse_message(datas: str) -> None:   
    global gaslevel 
    #glevel = array('B', [0,0,0])
    
    for data in datas:        
        decoded = data[3:].decode('utf-8')

        if data[:3] == b'LG1':
            gaslevel[0] = int(decoded)                    

        elif data[:3] == b'LG2':
            gaslevel[1] = int(decoded)                  

        elif data[:3] == b'LG3':
            gaslevel[2] = int(decoded)                   
       # print("Gaz level 123 ", gaslevel, datetime.datetime.now().time())
    

def Send_message(msg):         
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT2))
        s.sendall(bytes(msg,'utf-8')) #'AG1M\r\nAG2L\r\nAG3H'  

def Send_command(cmd):         
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT2))
        s.sendall(bytes(cmd,'utf-8')) #'AG1M\r\nAG2L\r\nAG3H'  

def Read_gas_level_task():
       
    print('waiting for server on ...port:' + format(PORT1))   
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT1))
        while True:
            data = s.recv(1024)
            # split socket message into array of consistent progammer readable data
            # b'LG1XX\r\nLG2YY\r\n' => b'[LG1XX,LG2YY]'
            msg = data.split(b'\r\n')
            
            #with threadLock:
            #threadLock.acquire()          
            parse_message(msg) #gaslevel = service.parse_message(msg)            
            print(f'T1 - Reading gaz level : {msg}' )            
            #threadLock.release()
            
            #print(f'T1 - Reading gaz level read : {msg}' ) # + str(gaslevel).strip('[]'))
            time.sleep(1)


def Send_command_task():
    global gaslevel
    
    # To do
    # depending on gasLevel value send the appropriate command
    cmd = 'VL1\r\n' #'IG2\r\nIG3\r\nIG1\r\n'  'AL1\r\n'
    
    while True:
        #if max(gaslevel) > 5:
        Send_command(cmd)
        print(f'T2 - Sending command: {cmd}')
        time.sleep(1.2)
        
    #To do    
    # if gasLevel value = 0 send appropriate command to Cancel previous command


def Send_alarm_task():
    global gaslevel    
    
    while True:
        #with threadLock:
        #threadLock.acquire()
        alert = service.displayAlert(gaslevel)
        if alert:
            print(f'T3 - Sending alert: {alert}')
            #Send_message(alert)
        #threadLock.release()
        #service.displayAlert(gaslevel)
        time.sleep(2)     


with concurrent.futures.ThreadPoolExecutor() as executor:
    f1 = executor.submit(Read_gas_level_task)    
    f2 = executor.submit(Send_command_task)
    f3 = executor.submit(Send_alarm_task)