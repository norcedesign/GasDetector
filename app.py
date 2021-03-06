import sys
import time
import socket
import threading

from array import*
from threading import Semaphore, Thread
from sense_emu import SenseHat
from colors import colors

sense = SenseHat()
sense.clear()

red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
yellow = (255, 255, 0)


gasLevel = array('B',[10,25,75]) # hardcodé just pour tester

def display(gas)-> None:
    global sense
    if gas >= 50:
        #sense.clear(red)
        sense.show_message(str(gas), text_colour=red)        
        print(f'{colors.RED}Alerte niveau 3!{colors.END}')
        #blank
    elif gas < 50 and gas >= 21:
        #sense.clear(yellow)
        sense.show_message(str(gas), text_colour=yellow)
        print(f'{colors.YELLOW}Alerte niveau 2!{colors.END}')
        
    elif gas< 21 and gas > 5:
        #sense.clear(green)
        sense.show_message(str(gas), text_colour=green)        
        print(f'{colors.GREEN}Alerte niveau 1!{colors.END}')


def Read_gas_level_task():
    global gasLevel
    print('reading gaz level: ' + str(gasLevel))
    time.sleep(0.1)
    #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s1:
    #    s1.connect((HOST, PORT1))
    #    while True: 
    #        data = s1.recv(1024)
    #        print('Received', repr(data))
            
def Send_alarm_task():
    global gasLevel
    print('Sending alert ... \n')
    for i in gasLevel:
        display(i)    
        time.sleep(0.1)
    

def Send_command_task():
    global gasLevel
    # depending on gasLevel value send the appropriate command
    print('Sending command: AL2...')
    
    # if gasLevel value = 0 send appropriate command to Cancel previous command
    
    time.sleep(0.2)

if __name__=="__main__":
    
    t1 = threading.Thread(target=Read_gas_level_task)
    t2 = threading.Thread(target=Send_alarm_task())
    t3 = threading.Thread(target=Send_command_task()) 
    t1.start()
    t2.start()
    t3.start()
    

