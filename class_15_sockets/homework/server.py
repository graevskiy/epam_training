import pathlib
import selectors
import socket
from collections import defaultdict
from multiprocessing import Lock
from multiprocessing.pool import ThreadPool

HOST = "localhost"
PORT = 9999

selector = selectors.DefaultSelector()
pool = ThreadPool(4)
bufs = defaultdict(bytes)
clients = defaultdict(str)
lock = Lock()


def append_data(data):
    data = data.decode()
    pathlib.Path("outputs").mkdir(parents=True, exist_ok=True)
    with lock:
        print("writing to a file")
        with open(f"outputs/output.txt", "a", encoding="utf-8") as f:
            f.write(data)
            f.write("\n")


def server(host, port):
    serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serv_sock.bind((host, port))
    serv_sock.listen(5)
    serv_sock.setblocking(False)
    selector.register(fileobj=serv_sock, events=selectors.EVENT_READ, data=accept_conn)


def accept_conn(serv_sock):
    client, addr = serv_sock.accept()
    print("Connection from", addr)
    client.setblocking(False)
    selector.register(fileobj=client, events=selectors.EVENT_READ, data=recv_message)


def recv_message(client_sock):
    addr = client_sock.getpeername()
    try:
        req = client_sock.recv(1024)
        if req:
            bufs[client_sock] += req
        else:
            selector.unregister(client_sock)
            print(f"Closing conn from {addr} normally")
            client_sock.close()
            data = bufs.pop(client_sock)
            pool.apply_async(append_data, (data,))
    except ConnectionError:
        selector.unregister(client_sock)
        print(f"Closing conn from {addr} w/ exception")
        client_sock.close()


def event_loop():
    try:
        while True:
            events = selector.select(0)

            for key, _ in events:
                callback = key.data
                callback(key.fileobj)
    except KeyboardInterrupt:
        print("keyboard interrupt occurred")
    finally:
        selector.close()


if __name__ == "__main__":
    server(HOST, PORT)
    event_loop()
