import re

from urllib.parse import urlparse, urldefrag, urljoin
from bs4 import BeautifulSoup
from data_crawler import DataCrawler, Response
from constants import (
    LOW_VALUE_SIZE,
    VALID_URLS, 
    BLACKLISTED_URLS, 
    MAX_HTTP_BYTES_SIZE, 
    LINK_DUMP_PATH, 
    FILE_EXTENSIONS,
    PATH_SEGMENTS,
    LINK_DUMP_STRUCTURE)
from parser_utils import tokenize
from json_utils import load_or_initialize_json, write_json
from typing import List, Tuple, Dict



dc = DataCrawler()



def scraper(url: str, resp: Response) -> List[str]:
    """
    Main function to scrape a given URL and process its links.

    Args:
        url (str): The URL to be scraped.
        resp (Response): The response object containing status and raw response.

    Returns:
        List[str]: A list of valid links found on the page.
    """
    url = url.lower()
    link_dump = load_or_initialize_json(LINK_DUMP_PATH, LINK_DUMP_STRUCTURE)
    valid_links = []

    # Check if the seed page has already been visited
    if is_seed_page_visited(url, link_dump):
        print("\tSeed page already visited, skipping\n")
        return []

    # Validate the seed page
    if not validate_seed_page(url, link_dump):
        print("\tSeed page is not valid, skipping\n")
        return []

    # Check if the link is of low value
    if low_value_link(resp):
        print("\tLink is of low value, skipping\n")
        return []

    # Extract and validate links from the seed page
    links = extract_next_links(url, resp)
    valid_links = validate_links(links, link_dump)

    # Process the valid links if the response is correct
    if dc.check_status_code_correct_crawl(resp):
        dc.get_page_crawled(valid_links)
        dc.scrape_words(url, resp)

    # Save the updated link dump to JSON
    write_json(LINK_DUMP_PATH, link_dump)

    return valid_links



def extract_next_links(url: str, resp: Response) -> List[str]:
    """
    Extract links from the response content.

    Args:
        url (str): The URL of the page being scraped.
        resp (Response): The response object containing status and raw response.

    Returns:
        List[str]: A list of extracted links.
    """
    next_links = []
    if dc.check_status_code_correct_crawl(resp):
        parsed = urlparse(url)
        host = f"https://{parsed.netloc}"
        soup = BeautifulSoup(resp.raw_response.content, 'html.parser')

        # Extract and defragment links
        for link in soup.find_all('a', href=True):
            link_defrag = urldefrag(urljoin(host, link['href']))[0]
            next_links.append(link_defrag)
    else:
        print(f"\tStatus Code: {resp.status} is not between 200 - 399 | No data | Size > {MAX_HTTP_BYTES_SIZE // 1000000} MB\n")

    return next_links



def is_valid(url: str) -> Tuple[bool, str]:
    """
    Check if a URL is valid based on predefined rules.

    Args:
        url (str): The URL to be validated.

    Returns:
        Tuple[bool, str]: A tuple containing a boolean indicating validity and a reason string.
    """
    try:
        parsed = urlparse(url)

        # Check for spaces in the netloc (edge case)
        if ' ' in parsed.netloc:
            return False, "Has spaces in the netloc"

        # Check if URL follows http(s) scheme
        if parsed.scheme not in {"http", "https"}:
            return False, "Does not follow http(s) scheme"

        # Check if URL is within allowed domains
        if not any(domain in parsed.netloc for domain in VALID_URLS):
            return False, "Does not follow domains and paths mentioned in the spec"

        # Check if URL is blacklisted
        if any(bl in url for bl in BLACKLISTED_URLS):
            return False, "Is on the blacklist"

        # Check for illegal file extensions
        invalid_link = re.match(FILE_EXTENSIONS, parsed.path.lower())
        if invalid_link:
            return False, "Has invalid extensions"

        # Check for specific path segments indicating document uploads
        if any(segment in parsed.path.lower() for segment in PATH_SEGMENTS):
            return False, "Contains path segments indicating document uploads"

        return True, "OK"

    except TypeError:
        print(f"\tTypeError for {parsed}\n")
        raise



def is_seed_page_visited(url: str, link_dump: Dict) -> bool:
    """
    Check if the seed page has already been visited.

    Args:
        url (str): The URL of the seed page.
        link_dump (Dict): The link dump data.

    Returns:
        bool: True if the seed page has been visited, False otherwise.
    """
    return url in link_dump['Seed']['Good'] or url in link_dump['Seed']['Bad']



def validate_seed_page(url: str, link_dump: Dict) -> bool:
    """
    Validate the seed page and update the link dump.

    Args:
        url (str): The URL of the seed page.
        link_dump (Dict): The link dump data.

    Returns:
        bool: True if the seed page is valid, False otherwise.
    """
    seed_valid, seed_reason = is_valid(url)
    link_dump['Seed']['Good' if seed_valid else 'Bad'][url] = seed_reason
    if not seed_valid:
        write_json(LINK_DUMP_PATH, link_dump)
    return seed_valid



def validate_links(links: List[str], link_dump: Dict) -> List[str]:
    """
    Validate the extracted links and update the link dump.

    Args:
        links (List[str]): The list of extracted links.
        link_dump (Dict): The link dump data.

    Returns:
        List[str]: A list of valid links.
    """
    valid_links = []
    for link in links:
        validity, reason = is_valid(link)
        if validity:
            valid_links.append(link)
        link_dump['Legal' if validity else 'Removed'][link] = reason
    return valid_links



def low_value_link(response: Response) -> bool:
    """
    Check if a link is of low value based on predefined rules.

    Args:
        url (str): The URL to be checked.

    Returns:
        bool: True if the link is of low value, False otherwise.
    """
    soup = BeautifulSoup(response.raw_response.content, 'html.parser')
    tokens = tokenize(soup.text)
    return len(tokens) < LOW_VALUE_SIZE