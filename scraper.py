import re

from urllib.parse import urlparse, urldefrag, urljoin
from bs4 import BeautifulSoup
from helper import Helper
from constants import VALID_URLS, BLACKLISTED_URLS, MAX_HTTP_BYTES_SIZE
from json_utils import load_or_initialize_json, write_json

helper = Helper()


def scraper(url, resp):
    link_dump = load_or_initialize_json('./data/link_dump.json', {'Legal': {}, 'Removed': {}})
    valid_links = []

    links = extract_next_links(url, resp)
    
    for link in links:
        validity, reason = is_valid(link)
        if validity:
            valid_links.append(link)
        link_dump['Legal' if validity else 'Removed'][link] = reason

    if helper.check_status_code_correct_crawl(resp):
        helper.get_page_crawled(valid_links)
        helper.scrape_words(url, resp)

    write_json('./data/link_dump.json', link_dump)

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

    if helper.check_status_code_correct_crawl(resp):
        parsed = urlparse(url)
        host = f"https://{parsed.netloc}"
        soup = BeautifulSoup(resp.raw_response.content, 'html.parser')

        # Defrag links
        for link in soup.find_all('a', href=True):
            link_defrag = urldefrag(urljoin(host, link['href']))[0]
            # clean_link = link_defrag.split('?')[0]
            next_link.append(link_defrag)
    else:
        print(f"\tStatus Code: {resp.status} is not between 200 - 399 / No data / Size > {MAX_HTTP_BYTES_SIZE}")

    return next_link



def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False, f"Does not follow http(s) scheme"

        if not any(domain in parsed.netloc for domain in VALID_URLS):
            return False, f"Does not follow domains and paths mentioned in the spec"

        if any(bl in url for bl in BLACKLISTED_URLS):
            return False, f"Is on the blacklist"

        invalid_extensions = (
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpg|mpeg|ram|m4v|mkv|ogg|ogv|pdf|bam|sam"
            + r"|ps|eps|tex|ppt|ppsx|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1|odc|scm"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|war|zip|rar|gz|z|zip)$"
        )

        valid_link = re.match(invalid_extensions, parsed.path.lower())
        
        return not valid_link, f"Has invalid extensions" if valid_link else f"OK"

    except TypeError:
        print(f"TypeError for {parsed}")
        raise