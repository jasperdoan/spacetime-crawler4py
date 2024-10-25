import scraper
import time

from threading import Thread
from inspect import getsource
from utils.download import download
from utils import get_logger
from urllib.parse import urlparse

class Worker(Thread):
    def __init__(self, worker_id, config, frontier, domain):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.worker_id = worker_id
        self.config = config
        self.frontier = frontier
        self.domain = domain
        super().__init__(daemon=True)
        
    def run(self):
        while True:
            tbd_url = self.frontier.get_tbd_url(self.domain)
            if not tbd_url:
                self.logger.info(f"Frontier is empty for domain {self.domain}. Stopping Worker-{self.worker_id}.")
                break
            
            self.enforce_politeness(tbd_url)
            
            resp = download(tbd_url, self.config, self.logger)
            self.logger.info(
                f"Downloaded {tbd_url}, status <{resp.status}>, "
                f"using cache {self.config.cache_server}.")
            scraped_urls = scraper.scraper(tbd_url, resp)
            for scraped_url in scraped_urls:
                self.frontier.add_url(scraped_url)
            self.frontier.mark_url_complete(tbd_url)
            time.sleep(self.config.time_delay)
    

    def enforce_politeness(self, url):
        """
        Lock is used here to enforce the 500ms politeness policy for domains. Each domain's last request time is 
        checked and updated in a critical section. Since this is a simple mutual exclusion scenario where the same 
        thread does not need to acquire the lock multiple times, a basic Lock is sufficient.
        """
        domain = urlparse(url).netloc
        with self.frontier.domain_lock:
            last_request_time = self.frontier.last_request_time.get(domain, 0)
            current_time = time.time()
            elapsed_time = current_time - last_request_time
            if elapsed_time < self.config.time_delay:
                sleep_time = self.config.time_delay - elapsed_time
                self.logger.info(f"Sleeping for {sleep_time:.2f} seconds to respect politeness for domain {domain}")
                time.sleep(sleep_time)
            self.frontier.last_request_time[domain] = time.time()