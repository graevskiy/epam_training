import argparse
import io
import logging
import os
import sys
import time
from contextlib import contextmanager
from functools import wraps
from multiprocessing import Lock
from multiprocessing.pool import ThreadPool
from pathlib import Path, PurePath
from typing import Any, Iterable, List, Tuple

import requests
from PIL import Image

# not sure how to set it up correctly. Used by `handle_image_processing` function
ProcessParams = Tuple[str, Tuple[int, int], int, Lock, Iterable[Tuple[int, int]]]

# set up logger
LOG_FORMAT = "%(levelname)s: '%(message)s'"
logging.basicConfig(format=LOG_FORMAT, level=logging.INFO, stream=sys.stdout)


# utility functions
@contextmanager
def move_to_dir(path: Path) -> None:
    """Context manager for getting into a provided directory"""

    tmp_path = os.getcwd()
    os.chdir(path)
    try:
        logging.debug(f"Moving into {path}")
        yield
    finally:
        logging.debug(f"Moving back into {tmp_path}")
        os.chdir(tmp_path)


def time_it(func):
    """Wrapper to measure time spent inside a function `func`"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        value = func(*args, **kwargs)
        spent_time = round(time.time() - start, 2)
        logging.info(f"Time spent in '{func.__name__}': {spent_time}")
        return value

    return wrapper


# functions for getting images
def get_urls(file: str) -> List:
    """Read `file` and make a list of urls out of it

    :param file: file with urls one per line
    :return: list of urls from `file`
    """

    logging.debug(f"Getting urls from {file}")
    with open(file, "r", encoding="utf-8") as f:
        urls = f.read().splitlines()
    return urls


def validate_response(response: Any) -> Tuple[bool, str]:
    """Checks http status code and Content-Type

    :param response: `requests.response` object returned from a given url
    :return: (0) whether response is valid and (1) appropriate message
    """

    # need to return messages so that url and message get logged i nthe same place
    # otherwise lock gets released and logger outputs messed up
    if response.status_code != 200:
        return False, f"response code: {response.status_code}"
    content_type = response.headers["Content-Type"]
    if content_type.split("/")[0] != "image":
        return False, f"wrong content type: {content_type}"
    return True, f"successfully downloaded {len(response.content)} bytes"


def get_content(url: str) -> bytes:
    """Sends GET request to a given url. Logs progress and return
    response in bytes (empty bytes sequence if request failed)

    :param url: url address that stores the image
    :return: bytes sequence (zero-length if failure)
    """

    try:
        with requests.get(url, timeout=(1.05, 3.05)) as r:
            is_valid, msg = validate_response(r)
            logging.info(f"GET: {url}\n{msg}")
            if is_valid:
                return r.content
    except requests.exceptions.RequestException:
        logging.info(f"GET: {url}\nError occurred, skipping this url")

    return b""


# manipulating w/ images
def resize_save_img(buf: bytes, size: Tuple[int, int], n: int) -> None:
    """Given bytes, turn it to an image, compress it to required format (`size`)
    ands saves in current directory in jpeg format.

    :param buf: bytes representing downloaded image
    :param size: maximum allowed dimensions for output image
    :param n: serial number used for output file name
    """

    buf = io.BytesIO(buf)
    with Image.open(buf) as im:
        im.thumbnail(size)
        if im.mode != "RGB":
            im = im.convert("RGB")
        im.save(f"thumb-{n}.jpg", "JPEG")


# preparing for processing images
def create_output_folder(path_name: str) -> Path:
    """Creates (if needed) a directory if needed

    :param path_name: path to directory
    :return: Path object representing a directory
    """

    path = Path(path_name)
    logging.debug("Creating output folder")
    path.mkdir(parents=True, exist_ok=True)
    return path


def convert_thumb_size_param(size: str) -> Tuple[int, int]:
    """Given `size` string from cl arguments, turn them into ints
    (width, height)

    :param size: should be a string looking like NxM where N,M are ints
    :return: tuple of ints: width and height, if successfully converted. Exit program otherwise
    """
    try:
        width, height = map(int, size.lower().split("x"))
    except ValueError:
        logging.error("Invalid `size` parameter provided")
        sys.exit(1)
    else:
        if min(width, height) < 1:
            logging.error(
                "Both width and height in `size` parameter should be positive"
            )
            sys.exit(1)
    return width, height


def validate_args(args: argparse.Namespace) -> None:
    """Validate most of provided CL arguments, exit program with logged error
    if something invalid found. Note, `size` CL parameter is validated separately.

    :param args: namespace from `argparse` module containing provided arguments
    :return: None
    """

    # validate file name
    if not Path(args.urls_file).is_file():
        logging.error("Invalid input file with urls")
        sys.exit(1)

    # validate size parameter
    if not args.size:
        logging.error("Invalid 'size' parameter provided")
        sys.exit(1)

    # validate path
    path = Path(args.dir)
    if path.exists() and not path.is_dir():
        path_ins = path if path.is_absolute() else PurePath.joinpath(path.cwd(), path)
        logging.error(f"Output directory '{path_ins}' can't be created")
        sys.exit(1)

    # validate threads #
    if args.threads < 1:
        logging.error("Threads number should be positive.")
        sys.exit(1)


def setup_arg_parser():
    """Setting CL arguments """

    parser = argparse.ArgumentParser(description="Thumbnails generator")
    parser.add_argument("urls_file", type=str, help="text file with urls")
    parser.add_argument(
        "--dir",
        "-d",
        type=str,
        default=Path.cwd(),
        help="output directory. default: cwd",
    )
    parser.add_argument(
        "--threads",
        "-t",
        type=int,
        default=1,
        help="number of threads (positive int). default: 1",
    )
    parser.add_argument(
        "--size",
        "-s",
        type=str,
        default="100x100",
        dest="img_dims",
        help="thumbnail dimensions (maximum values)",
    )

    return parser.parse_args()


# main processing handler
def handle_image_processing(params: ProcessParams) -> None:
    """Wrapper for all functionality related to image processing.
    Allowing to send it to a thread. Ugly parametrization.

    :param params: tuple of several items:
        - url: string representing url where original image stored
        - size: width, height for future thumbnail
        - n: serial number of newly created thumbnail
        - lock: Lock object to acquire for updating counts
        - glob_count: pair of counters - urls successfully processed, number of bytes downloaded
    :return: None
    """
    url, size, n, lock, glob_count = params

    img_from_url = get_content(url)

    if img_from_url:
        resize_save_img(img_from_url, size, n)
        success_count, bytes_count = 1, len(img_from_url)

        lock.acquire()
        # need to update values in place
        glob_count[0] += success_count
        glob_count[1] += bytes_count
        lock.release()


@time_it
def main():
    """Main function holding all business logic"""

    # parse cli arguments
    args = setup_arg_parser()

    # convert input value
    args.size = convert_thumb_size_param(args.img_dims)

    # validate
    validate_args(args)

    # make output folder and extract urls from input file
    output_path = create_output_folder(args.dir)
    urls = get_urls(args.urls_file)

    # moving to needed output directory
    with move_to_dir(output_path):

        # create lock for counters and thread pool of workers
        lock = Lock()
        pool = ThreadPool(args.threads)
        counter = [0, 0]

        # create iterable of parameters for handler and submit all them to the pool
        process_params = (
            (url, args.size, n, lock, counter) for n, url in enumerate(urls, start=1)
        )
        pool.map(handle_image_processing, process_params)

        # close pool so nobody can submit tasks and force main thread to live until all done
        pool.close()
        pool.join()

    # log necessary statistics
    num_successes, overall_num_bytes = counter
    logging.info(f"Number of bytes downloaded: {overall_num_bytes}")
    logging.info(f"Number of images successfully processed: {num_successes}")
    logging.info(f"Number of fails: {len(urls) - num_successes}")


if __name__ == "__main__":
    main()
