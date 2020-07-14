import socket
import time

import psutil
import pyautogui

from metric import Metric

HOST = "localhost"
PORT = 9999
TIME_FORMAT = "%m/%d/%Y %H:%M:%S"
SLEEP_TIME = 10


class ConnException(Exception):
    pass


def client_send(host, port, data):

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        print(f"Connected to {host}:{port}")
    except ConnectionError:
        print("Connection error occurred")
        return

    time_ = time.strftime(TIME_FORMAT, time.localtime())
    data = f"{time_}: {data}".encode("utf-8")
    with sock:
        msg_len = len(data)
        print("sending data:", data)
        while msg_len:
            num_sent = sock.send(data)
            msg_len -= num_sent
            if not num_sent:
                raise ConnException("Connection failed.")
    print("Socket closed")


if __name__ == "__main__":
    mouse = Metric("mouse", pyautogui.position)
    cpu = Metric("cpu", psutil.cpu_percent)

    metrics = [mouse, cpu]
    for m in metrics:
        m.start_collect()

    while True:
        try:
            # maybe need to do another step of processing
            # to calculate aggregated data
            data = ";".join([f"{m.get_current_state()}" for m in metrics])
            for m in metrics:
                m.cleanup()
            client_send(HOST, PORT, data)
            time.sleep(SLEEP_TIME)
        except KeyboardInterrupt:
            print("Interrupted")
            break

    for m in metrics:
        m.stop_collect()
