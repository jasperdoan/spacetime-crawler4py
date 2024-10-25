import os
import shelve

from threading import Thread, RLock, Lock
from queue import Queue, Empty
from utils import get_logger, get_urlhash, normalize
from scraper import is_valid
from urllib.parse import urlparse
from collections import defaultdict, deque

class Frontier(object):
    def __init__(self, config, restart):
        self.logger = get_logger("FRONTIER")
        self.config = config
        self.domain_queues = defaultdict(Queue)
        self.domain_order = deque()
        self.lock = RLock()                 # Reader-writer lock
        self.domain_lock = Lock()           # Lock for domain politeness
        self.last_request_time = {}         # Dictionary to store last request time for each domain
        
        if not os.path.exists(self.config.save_file) and not restart:
            self.logger.info(
                f"Did not find save file {self.config.save_file}, "
                f"starting from seed.")
        elif os.path.exists(self.config.save_file) and restart:
            self.logger.info(
                f"Found save file {self.config.save_file}, deleting it.")
            os.remove(self.config.save_file)
        
        self.save = shelve.open(self.config.save_file)
        if restart:
            for url in self.config.seed_urls:
                self.add_url(url)
        else:
            self._parse_save_file()
            if not self.save:
                for url in self.config.seed_urls:
                    self.add_url(url)

    def _parse_save_file(self):
        total_count = len(self.save)
        tbd_count = 0
        with self.lock:
            for url, completed in self.save.values():
                if not completed and is_valid(url):
                    self.add_url(url)
                    tbd_count += 1
        self.logger.info(
            f"Found {tbd_count} urls to be downloaded from {total_count} "
            f"total urls discovered.")

    def get_tbd_url(self):
        with self.lock:
            if not self.domain_order:
                return None
            for _ in range(len(self.domain_order)):
                domain = self.domain_order.popleft()
                try:
                    url = self.domain_queues[domain].get_nowait()
                    self.domain_order.append(domain)
                    return url
                except Empty:
                    continue
            return None

    def add_url(self, url):
        url = normalize(url)
        urlhash = get_urlhash(url)

        parsed_url = urlparse(url)
        domain = parsed_url.netloc.split('.', 1)[1]
        
        with self.lock:
            if urlhash not in self.save:
                self.save[urlhash] = (url, False)
                self.save.sync()
                self.domain_queues[domain].put(url)
                if domain not in self.domain_order:
                    self.domain_order.append(domain)
    
    def mark_url_complete(self, url):
        urlhash = get_urlhash(url)
        with self.lock:
            if urlhash not in self.save:
                self.logger.error(
                    f"Completed url {url}, but have not seen it before.")
            self.save[urlhash] = (url, True)
            self.save.sync()