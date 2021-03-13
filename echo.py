import socket


def client(host: str = 'localhost', port: int = 1234) -> socket:
    screen: socket
    screen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    screen.connect((host, port))
    return screen


def server(host: str = 'localhost', port: int = 1234):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        while True:
            data = s.recv(1024)
            print('Received', data)




