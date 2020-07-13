from typing import List, Tuple
from queue import Queue
from multiprocessing.pool import ThreadPool
import logging
import requests
import io
import os
import time
from PIL import Image
import threading
import multiprocessing

logging.basicConfig(level=logging.INFO)


class Task:
    slots = ('n', 'buf', 'func', 'url')

    def __init__(self, n, buf, func, url):
        self.n = n
        self.buf = buf
        self.func = func
        self.url = url

    def __repr__(self):
        return f"<Task func={self.func}>"

def get_urls(file: str) -> List:
    """Read `file` and make a list of urls out of it

    :param file: file with urls one per line
    :return: list of urls from `file`
    """

    logging.debug(f"Getting urls from {file}")
    with open(file, "r", encoding="utf-8") as f:
        urls = f.read().splitlines()
    return urls


def get_content(url: str) -> bytes:
    """Sends GET request to a given url. Logs progress and return
    response in bytes (empty bytes sequence if request failed)

    :param url: url address that stores the image
    :return: bytes sequence (zero-length if failure)
    """

    try:
        with requests.get(url, timeout=(1.05, 3.05)) as r:
            return r.content
    except requests.exceptions.RequestException:
        logging.info(f"GET: {url}\nError occurred, skipping this url")

    return b""


# manipulating w/ images
def resize_save_img(buf: bytes, n: int) -> None:
    """Given bytes, turn it to an image, compress it to required format (`size`)
    ands saves in current directory in jpeg format.

    :param buf: bytes representing downloaded image
    :param size: maximum allowed dimensions for output image
    :param n: serial number used for output file name
    """

    buf = io.BytesIO(buf)
    with Image.open(buf) as im:
        im.thumbnail((100, 100))
        if im.mode != "RGB":
            im = im.convert("RGB")
        im.save(f"thumb-{n}.jpg", "JPEG")


def handle2():
    logging.info(f'Consumer thread start: {threading.current_thread().name}')
    for task in iter(q.get, None):
        logging.info(f'thread handle2 {threading.current_thread().name}\ngetting from q {task}')
        task.func(task.buf, task.n)
        q.task_done()


def handle(task):

    logging.info(f'Producer thread start: {threading.current_thread().name}')
    task.buf = task.func(task.url)
    if task.buf:
        task.func = resize_save_img
        q.put(task)
        logging.info(f'thread handle {threading.current_thread().name}\n put in q {task}')



if __name__ == '__main__':

    print('main process', os.getpid())

    filename = 'urls.txt'
    urls = get_urls(filename)
    urls = [Task(i, b'', get_content, url) for i, url in enumerate(urls, start=1)]

    tmp_dir = os.getcwd()
    os.chdir('output')

    q = Queue()

    pool2 = ThreadPool(processes=4, initializer=handle2)

    pool = ThreadPool(4)
    pool.map(handle, urls)

    pool.close()
    pool.join()

    # join queue only after all tasks were submitted
    q.join()

    for t in threading.enumerate():
        print(t)
    os.chdir(tmp_dir)
