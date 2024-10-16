import re

from urllib.parse import urlparse, urldefrag, urljoin
from bs4 import BeautifulSoup
from helper import Helper
from constants import VALID_URLS, BLACKLISTED_URLS, MAX_HTTP_BYTES_SIZE


helper = Helper()


def scraper(url, resp):
    links = extract_next_links(url, resp)
    valid_links = [link for link in links if is_valid(link)]

    # Check resp status between 2xx : Success & 3xx : Redirection
    # Check if the response has data and is less than MAX_HTTP_BYTES_SIZE
    if helper.check_status_code_correct_crawl(resp):
        helper.get_page_crawled(valid_links)
        helper.scrape_words(url, resp)

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

    # Check resp status between 2xx : Success & 3xx : Redirection
    # Check if the response has data and is less than MAX_HTTP_BYTES_SIZE
    if helper.check_status_code_correct_crawl(resp):
        parsed = urlparse(url)
        host = f"https://{parsed.netloc}"
        soup = BeautifulSoup(resp.raw_response.content, 'html.parser')

        next_link = [
            urldefrag(urljoin(host, link['href']))[0]
            for link in soup.find_all('a', href=True)
        ]
    else:
        print(f"Status Code: {resp.status} is not between 200 - 399 / No data / Size > {MAX_HTTP_BYTES_SIZE}")

    return next_link



def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False

        if not any(domain in parsed.netloc for domain in VALID_URLS):
            return False

        if any(bl in url for bl in BLACKLISTED_URLS):
            return False

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
        
        return not re.match(invalid_extensions, parsed.path.lower())

    except TypeError:
        print(f"TypeError for {parsed}")
        raise