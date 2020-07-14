import socket
import time
import random

HOST = 'localhost'
PORT = 9999
TIME_FORMAT = "%m/%d/%Y %H:%M:%S"
SLEEP_TIME = 1


class ConnException(Exception):
    pass


def client(host, port):

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
    except ConnectionError:
        print('Connection error occurred')
        return

    time_ = time.strftime(TIME_FORMAT, time.localtime())
    data = f'{time_} {random.randrange(100)}'
    data = data.encode('utf-8')
    with sock:
        msg_len = len(data)
        while msg_len:
            num_sent = sock.send(data)
            msg_len -= num_sent
            print(num_sent)
            if not num_sent:
                raise ConnException("Connection failed.")
    print('Socket closed')


if __name__ == '__main__':
    while True:
        try:
            client(HOST, PORT)
            time.sleep(SLEEP_TIME)
        except KeyboardInterrupt:
            print('Interrupted')
            break
