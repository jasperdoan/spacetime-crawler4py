import os
import time
import logging

from hashlib import sha256
from urllib.parse import urlparse


class ElapsedTimeFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, style='%'):
        super().__init__(fmt, datefmt, style)
        self.start_time = time.time()

    def formatTime(self, record, datefmt=None):
        elapsed_seconds = record.created - self.start_time
        hours, remainder = divmod(elapsed_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = (seconds - int(seconds)) * 1000

        time_str = ""
        if hours >= 1:
            time_str += f"{int(hours)}h"
        if minutes >= 1:
            time_str += f"{int(minutes)}m"
        time_str += f"{int(seconds)}.{int(milliseconds):03}s"

        return time_str


def get_logger(name, filename=None):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not os.path.exists("Logs"):
        os.makedirs("Logs")
    fh = logging.FileHandler(f"Logs/{filename if filename else name}.log")
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = ElapsedTimeFormatter(
       "%(asctime)s | %(name)s | %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


def get_urlhash(url):
    parsed = urlparse(url)
    # everything other than scheme.
    return sha256(
        f"{parsed.netloc}/{parsed.path}/{parsed.params}/"
        f"{parsed.query}/{parsed.fragment}".encode("utf-8")).hexdigest()

def normalize(url):
    if url.endswith("/"):
        return url.rstrip("/")
    return url