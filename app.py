import sys
import time
import socket
import threading

from array import *
from threading import Semaphore, Thread
from sense_emu import SenseHat
from colors import colors

HOST: str = '192.168.2.199'  # update to the desired ip address
PORT: int = 1234  # update to the desired port
PORT1: int = 14712  # update to the desired port
PORT2: int = 47319  # update to the desired port

sense = SenseHat()
sense.clear()

red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
yellow = (255, 255, 0)

gasLevel = array('B', [10, 25, 75])  # hardcodé just pour tester
gas1 = LG1 = 0
gas2 = LG2 = 0
gas3 = LG3 = 0


def display(gas) -> None:
    global sense
    if gas >= 50:
        # sense.clear(red)
        sense.show_message(str(gas), text_colour=red)
        print(f'{colors.RED}Alerte niveau 3!{colors.END}')
        # blank
    elif gas < 50 and gas >= 21:
        # sense.clear(yellow)
        sense.show_message(str(gas), text_colour=yellow)
        print(f'{colors.YELLOW}Alerte niveau 2!{colors.END}')

    elif gas < 21 and gas > 5:
        # sense.clear(green)
        sense.show_message(str(gas), text_colour=green)
        print(f'{colors.GREEN}Alerte niveau 1!{colors.END}')


# parse splite socket data (e.g: b'[LG1XX,LG2YY]')
# socket datas are encode in bytes by default
def parse_message(datas: str) -> None:
    # print(datas)
    # b'[LG1XX,LG2YY]'
    for data in datas:
        # b'XX => 'XX' bytes to string
        decoded = data[3:].decode('utf-8')

        if data[:3] == b'LG1':
            gas1 = LG1 = int(decoded)
            print("GAS 1 : ", gas1)#comment this line if necessary
            Send_alarm_task(gas1)

        elif data[:3] == b'LG2':
            gas2 = LG2 = int(decoded)
            print("GAS 2 : ", gas2)#comment this line if necessary
            Send_alarm_task(gas2)

        elif data[:3] == b'LG3':
            gas3 = LG3 = int(decoded)
            print("GAS 3 : ", gas3)#comment this line if necessary
            Send_alarm_task(gas3)


def Read_gas_level_task():
    global gasLevel
    print('reading gaz level: ' + str(gasLevel))
    print('waiting as server on ...port:' + format(PORT1))
    time.sleep(0.1)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT1))
        while True:
            data = s.recv(1024)
            # split socket message into array of consistent progammer readable data
            # b'LG1XX\r\nLG2YY\r\n' => b'[LG1XX,LG2YY]'
            msg = data.split(b'\r\n')
            parse_message(msg)


def Send_alarm_task(gasVal):
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


if __name__ == "__main__":
    t1 = threading.Thread(target=Read_gas_level_task)
    # t2 = threading.Thread(target=Send_alarm_task())
    # t3 = threading.Thread(target=Send_command_task())
    t1.start()
    # t2.start()
    # t3.start()



