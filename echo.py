import socket

readClient: socket
writeClient: socket


def connect(host: str = 'localhost', read: int = 1231, write: int = 1232) -> None:
    global readClient, writeClient

    readClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    readClient.connect((host, read))

    writeClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    writeClient.connect((host, write))


def send_message(msg: str) -> None:
    global writeClient
    writeClient.send(msg.encode('utf-8'))


def read_message() -> str:
    global readClient

    message = ''
    data = readClient.recv(1024)

    if data:
        message = data.decode('utf-8')

    return message
