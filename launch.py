from configparser import ConfigParser
from argparse import ArgumentParser
from utils.server_registration import get_cache_server
from utils.config import Config
from crawler.frontier import Frontier
from crawler.worker import Worker

def main(config_file, restart):
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