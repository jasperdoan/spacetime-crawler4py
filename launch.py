import os
import json
from configparser import ConfigParser
from argparse import ArgumentParser
from utils.server_registration import get_cache_server
from utils.config import Config
from crawler.frontier import Frontier
from crawler.worker import Worker
from urllib.parse import urlparse
from constants import (
    DATA_DIR,
    LINK_DUMP_PATH,
    PAGE_CRAWLED_PATH,
    WORDS_STATS_PATH,
    LINK_DUMP_STRUCTURE,
    WORDS_STATS_STRUCTURE,
    PAGES_CRAWLED_STRUCTURE
)


def set_up_json():
    # Create the data directory if it does not exist
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    # Create the link dump file if it does not exist
    if not os.path.exists(LINK_DUMP_PATH):
        with open(LINK_DUMP_PATH, 'w') as link_dump_file:
            json.dump(LINK_DUMP_STRUCTURE, link_dump_file)

    # Create the page crawled file if it does not exist
    if not os.path.exists(PAGE_CRAWLED_PATH):
        with open(PAGE_CRAWLED_PATH, 'w') as page_crawled_file:
            json.dump(PAGES_CRAWLED_STRUCTURE, page_crawled_file)

    # Create the words stats file if it does not exist
    if not os.path.exists(WORDS_STATS_PATH):
        with open(WORDS_STATS_PATH, 'w') as words_stats_file:
            json.dump(WORDS_STATS_STRUCTURE, words_stats_file)


def main(config_file, restart):
    set_up_json()
    cparser = ConfigParser()
    cparser.read(config_file)
    config = Config(cparser)
    config.cache_server = get_cache_server(config, restart)
    frontier = Frontier(config, restart)
    
    workers = []
    for i in range(config.threads_count):
        worker = Worker(i, config, frontier)
        worker.start()
        workers.append(worker)
    
    for worker in workers:
        worker.join()

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--restart", action="store_true", default=False)
    parser.add_argument("--config_file", type=str, default="config.ini")
    args = parser.parse_args()
    main(args.config_file, args.restart)