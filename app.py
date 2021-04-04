import array
import concurrent.futures
import sys
import time

from colors import colors
from echo import connect, read_message, send_message
from sense_emu import SenseHat

sense: SenseHat
gasLevel: array.array

HOST: str = 'localhost'  # update to the desired ip address
READ_PORT: int = 1231  # update to the desired port
WRITE_PORT: int = 1232  # update to the desired port


def read_gas_level() -> None:
    global gasLevel

    while True:
        message = read_message()

        if message:
            data = message.splitlines()

            print(f'{colors.CYAN}T1 - Reading gas level : {data}{colors.END}')
            parse_message_data(data)

        time.sleep(1)


def parse_message_data(data: [str]) -> None:
    global gasLevel

    for datum in data:
        value = int(datum[3:])

        if datum[:3] == 'LG1':
            gasLevel[0] = value

        elif datum[:3] == 'LG2':
            gasLevel[1] = value

        elif datum[:3] == 'LG3':
            gasLevel[2] = value


def send_command() -> None:
    while True:
        cmd = get_command()

        if cmd:
            print(f'{colors.CYAN}T2 - Sending command: {cmd.splitlines()}{colors.END}')
            send_message(cmd)

        time.sleep(1.2)


def get_command() -> str:
    global gasLevel

    cmd = ''
    controlled = True

    for index, level in enumerate(gasLevel):
        if level >= 5:
            controlled = False

        if level <= 30:
            cmd += 'AIG' + str(index + 1) + '\r\n'

        if 5 < level <= 10:
            cmd += 'AL1' + '\r\n'
            cmd += 'VL1' + '\r\n'

        elif 10 < level <= 15:
            cmd += 'AL2' + '\r\n'
            cmd += 'VL1' + '\r\n'

        elif 15 < level <= 20:
            cmd += 'AL2' + '\r\n'
            cmd += 'VL2' + '\r\n'

        elif 20 < level <= 60:
            cmd += 'AL3' + '\r\n'
            cmd += 'VL2' + '\r\n'

        elif 60 < level <= 100:
            cmd += 'AL3' + '\r\n'
            cmd += 'VL2' + '\r\n'
            cmd += 'IG' + str(index + 1) + '\r\n'

    if controlled:
        cmd += 'VN' + '\r\n'

    return cmd


def send_alarm() -> None:
    while True:
        alert = display_alert()

        if alert:
            print(f'{colors.CYAN}T3 - Sending alert: {alert.splitlines()}{colors.END}')
            send_message(alert)

        time.sleep(2)


def display_alert() -> str:
    global gasLevel
    message = ''

    for index, level in enumerate(gasLevel):
        if 100 >= level > 50:
            print(f'{colors.RED}Alerte niveau 3!{colors.END}')
            message += 'AG' + str(index + 1) + 'H' + '\r\n'

        elif 50 >= level > 20:
            print(f'{colors.YELLOW}Alerte niveau 2!{colors.END}')
            message += 'AG' + str(index + 1) + 'M' + '\r\n'

        elif 20 >= level > 5:
            print(f'{colors.GREEN}Alerte niveau 1!{colors.END}')
            message += 'AG' + str(index + 1) + 'L' + '\r\n'

        elif 5 >= level >= 0:
            print(f'{colors.CYAN}Aucune alerte!{colors.END}')
            message += 'AG' + str(index + 1) + '' + '\r\n'

    return message


def show_level() -> None:
    global gasLevel

    while True:
        alert = 'L'
        color = 'green'

        for index, level in enumerate(gasLevel):
            if 100 >= level > 50:
                alert = 'H'
                color = 'red'

            elif 50 >= level > 20 and alert != 'H':
                alert = 'M'
                color = 'yellow'

        sense.set_pixels([[0, 0, 0]] * 64)
        time.sleep(0.02)

        sense.show_letter(alert, text_colour=colors.RGB[color])
        time.sleep(1.4)


def main() -> None:
    global sense, gasLevel

    sense = SenseHat()
    sense.clear()

    gasLevel = array.array('B', [0, 0, 0])
    connect(HOST, READ_PORT, WRITE_PORT)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(read_gas_level)
        executor.submit(send_command)
        executor.submit(send_alarm)
        executor.submit(show_level)


if __name__ == '__main__':
    try:
        main()
    except:
        print(f'{colors.GREEN}\nExiting application\n{colors.END}')
        sys.exit(0)
