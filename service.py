import sys
import time
#import socket
#import threading
import datetime
#import concurrent.futures


from array import *
#from threading import Semaphore, Thread
from sense_emu import SenseHat
from colors import colors

red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
yellow = (255, 255, 0)

sense = SenseHat()
sense.clear()

HOST: str = '192.168.1.107'  # update to the desired ip address
PORT: int = 1234  # update to the desired port
PORT1: int = 1231  # update to the desired port
PORT2: int = 1232  # update to the desired port

#gaslevel = array('B', [10,30,60])
#vide = True
#plein = False
#def displayRemote(msg):         
#    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#        s.connect((HOST, PORT2))
#        s.sendall(bytes(msg,'utf-8')) #'AG1M\r\nAG2L\r\nAG3H'

def displayAlert(glevel):
    #global sense #, gaslevel    
    
    alertMsg=''
    for x, gas in enumerate(glevel):
        if gas >= 50:
            # sense.clear(red)
            #sense.show_message(str(gaslevel[x]), text_colour=red)
            print(f'{colors.RED}Alerte niveau 3!{colors.END}')
            alertMsg += 'AG' + str(x+1) + 'H' +'\r\n'
            # blank
        elif gas  < 50 and gas >= 21:
            # sense.clear(yellow)
            #sense.show_message(str(gaslevel[x]), text_colour=yellow)
            print(f'{colors.YELLOW}Alerte niveau 2!{colors.END}')
            alertMsg += 'AG' + str(x+1) + 'M' +'\r\n'
            
        elif gas < 21 and gas > 5:
            # sense.clear(green)
            #sense.show_message(str(gaslevel[x]), text_colour=green)
            print(f'{colors.GREEN}Alerte niveau 1!{colors.END}')
            alertMsg += 'AG' + str(x+1) + 'L' +'\r\n'
    #displayRemote(alertMsg)
    return alertMsg

    
#gaslevel = array('B', [10, 30, 60])
#displayAlert()

def parse_message(datas: str) -> None:
    # print(datas)
    # b'[LG1XX,LG2YY]'
    #global gaslevel # plein, vide
    glevel = array('B', [0,0,0])
    
    for data in datas:
        # b'XX => 'XX' bytes to string
        decoded = data[3:].decode('utf-8')

        if data[:3] == b'LG1':
            gas1 = LG1 = int(decoded)
            glevel[0] = gas1
            #print("GAS 1 : ", gas1)#comment this line if necessary
            #displayAlert(gas1)           

        elif data[:3] == b'LG2':
            gas2 = LG2 = int(decoded)
            glevel[1] = gas2
            #print("GAS 2 : ", gas2)#comment this line if necessary
            #displayAlert(gas2)           

        elif data[:3] == b'LG3':
            gas3 = LG3 = int(decoded)
            glevel[2] = gas3
            #print("GAS 3 : ", gas3)#comment this line if necessary
            #Send_alarm_task(gas3)           
    
    print("Gaz level ", glevel, datetime.datetime.now().time())
    #return glevel

      