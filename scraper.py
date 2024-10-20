import re

from urllib.parse import urlparse, urldefrag, urljoin
from bs4 import BeautifulSoup
from data_crawler import DataCrawler
from constants import (
    VALID_URLS, 
    BLACKLISTED_URLS, 
    MAX_HTTP_BYTES_SIZE, 
    LINK_DUMP_PATH, 
    FILE_EXTENSIONS,
    LINK_DUMP_STRUCTURE)
from json_utils import load_or_initialize_json, write_json


dc = DataCrawler()


def scraper(url, resp):
    link_dump = load_or_initialize_json(LINK_DUMP_PATH, LINK_DUMP_STRUCTURE)
    valid_links = []

    # Set seed page, if not already visited. Skip if already visited
    if url in link_dump['Seed']['Good'] or url in link_dump['Seed']['Bad']:
        print(f"\tSeed page already visited, skipping\n")
        return []
    
    # Check if seed page is valid, if not log it and skip
    seed_valid, seed_reason = is_valid(url)
    link_dump['Seed']['Good' if seed_valid else 'Bad'][url] = seed_reason
    if not seed_valid:
        print(f"\tSeed page is not valid, skipping\n")
        write_json(LINK_DUMP_PATH, link_dump)
        return []

    # Grab links within seed page
    links = extract_next_links(url, resp)
    
    for link in links:
        validity, reason = is_valid(link)                               # Check if link is "valid"
        if validity:                                                    # If it is add it into valid links
            valid_links.append(link)
        link_dump['Legal' if validity else 'Removed'][link] = reason    # Log into link dump logs

    if dc.check_status_code_correct_crawl(resp):
        dc.get_page_crawled(valid_links)                            # Start page crawl
        dc.scrape_words(url, resp)                                  # Scape words within page

    # Logs legal/illegal url into json file
    write_json(LINK_DUMP_PATH, link_dump)

    return valid_links



def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    next_link = []

    if dc.check_status_code_correct_crawl(resp):
        parsed = urlparse(url)
        host = f"https://{parsed.netloc}"
        soup = BeautifulSoup(resp.raw_response.content, 'html.parser')

        # Defrag links
        for link in soup.find_all('a', href=True):
            link_defrag = urldefrag(urljoin(host, link['href']))[0]
            # clean_link = link_defrag.split('?')[0]
            next_link.append(link_defrag)
    else:
        print(f"\tStatus Code: {resp.status} is not between 200 - 399 | No data | Size > {MAX_HTTP_BYTES_SIZE//1000000} MB\n")

    return next_link



def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)

        # [Edge case] If inside netloc, there's a space, it's invalid
        if ' ' in parsed.netloc:
            return False, f"Has spaces in the netloc"

        # Check if url follows http(s) scheme
        if parsed.scheme not in set(["http", "https"]):
            return False, f"Does not follow http(s) scheme"

        # Check if url is within given specs (allowed links)
        if not any(domain in parsed.netloc for domain in VALID_URLS):
            return False, f"Does not follow domains and paths mentioned in the spec"

        # Check if its within black listed urls
        if any(bl in url for bl in BLACKLISTED_URLS):
            return False, f"Is on the blacklist"

        # Illegal file extensions
        invalid_link = re.match(FILE_EXTENSIONS, parsed.path.lower())
        
        return not invalid_link, f"OK" if not invalid_link else f"Has invalid extensions"

    except TypeError:
        print(f"TypeError for {parsed}")
        raise