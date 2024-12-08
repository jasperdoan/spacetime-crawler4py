from bs4 import BeautifulSoup
from constants import (
    MAX_HTTP_BYTES_SIZE,
    SIMHASH_THRESHOLD,
    WORDS_STATS_PATH,
    PAGE_CRAWLED_PATH, 
    SIMHASH_PATH,
    WORDS_STATS_STRUCTURE,
    PAGES_CRAWLED_STRUCTURE)
from json_utils import load_or_initialize_json, write_json
from parser_utils import tokenize, parse_url
from dataclasses import dataclass, field
from typing import Dict, Any
from simhash import SimHash



@dataclass
class Response:
    """
    Dataclass to store the response status and raw response content.
    """
    status: int
    raw_response: Any



@dataclass
class WordStats:
    """
    Dataclass to store word statistics.
    """
    Stats: Dict[str, Any] = field(default_factory=dict)
    URL_list: Dict[str, int] = field(default_factory=dict)
    Word_list: Dict[str, int] = field(default_factory=dict)



@dataclass
class PageCrawled:
    """
    Dataclass to store information about crawled pages.
    """
    Unique: Dict[str, Any] = field(default_factory=dict)
    Subdomains_List: Dict[str, Dict[str, int]] = field(default_factory=dict)
    Link_List: Dict[str, int] = field(default_factory=dict)



class DataCrawler:
    """
    Class to handle data crawling operations including checking response status,
    scraping words, and getting page crawled information.
    """
    def __init__(self):
        self.simhash = SimHash()
        self.visited_hashes = {}


    def check_status_code_correct_crawl(self, resp: Response) -> bool:
        """
        Check if the response status code is within the acceptable range for crawling.

        Args:
            resp (Response): The response object containing status and raw response.

        Returns:
            bool: True if the status code is between 200 and 399, the response has data,
                  and the content size is less than the maximum allowed size.
        """
        # Check if the status code is within the acceptable range for crawling 2xx: Success, 3xx: Redirection
        ok_status = 200 <= resp.status <= 399

        # Check if the response has data to begin with
        has_data = resp.raw_response is not None

        # Check if the content size is less than the maximum allowed size and has data
        less_than_max_size = len(resp.raw_response.content) <= MAX_HTTP_BYTES_SIZE if has_data else False

        return ok_status and has_data and less_than_max_size


    def scrape_words(self, url: str, resp: Response):
        """
        Scrape words from the response content and update word statistics.

        Args:
            url (str): The URL of the page being scraped.
            resp (Response): The response object containing status and raw response.
        """
        # Load or initialize word statistics
        ws = load_or_initialize_json(WORDS_STATS_PATH, WORDS_STATS_STRUCTURE)
        ws = WordStats(**ws)
        # download_nltk_library()
        sort_args = {'key': lambda item: item[1], 'reverse': True}
        
        # Parse the response content using BeautifulSoup
        soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
        
        # Tokenize the text content and remove stop words
        token_list = tokenize(soup.text)
        
        # Update URL list with the number of tokens
        ws.URL_list[url] = len(token_list)
        
        # Update word list with token frequencies
        for token in token_list:
            ws.Word_list[token] = ws.Word_list.get(token, 0) + 1
        
        # Sort URL list and update statistics for the longest page
        sorted_url_list = sorted(ws.URL_list.items(), **sort_args)
        ws.Stats['Longest_Page_(words)'] = {sorted_url_list[0][0]: sorted_url_list[0][1]}
        
        # Sort word list and update statistics for the 50 most common words
        sorted_words = sorted(ws.Word_list.items(), **sort_args)
        ws.Stats['50_Most_Common_Words'] = dict(sorted_words[:50])
        
        # Write updated word statistics to JSON file
        write_json(WORDS_STATS_PATH, ws.__dict__)


    def get_page_crawled(self, link_list: list):
        """
        Update page crawled information based on the provided list of links.

        Args:
            link_list (list): List of links to be processed.
        """
        # Load or initialize page crawled information
        pgc = load_or_initialize_json(PAGE_CRAWLED_PATH, PAGES_CRAWLED_STRUCTURE)
        pgc = PageCrawled(**pgc)
        
        for link in link_list:
            domain, subdomain, path = parse_url(link.lower())
            full_subdomain = f'{subdomain}.{domain}'
            domain_path = f'{domain}{path}'
            ics_domain_condition = domain == 'ics.uci.edu' and subdomain != 'www'
            
            # Update subdomains list and unique subdomains for ICS domain
            if ics_domain_condition and subdomain not in pgc.Subdomains_List:
                pgc.Subdomains_List[subdomain] = {domain_path: 1}       # If the subdomain is not already in the list, add it with the domain path
                pgc.Unique['ICS_Subdomains'][full_subdomain] = 1        # Initialize the count for the full subdomain in the unique subdomains list

            elif ics_domain_condition:
                visited = domain_path in pgc.Subdomains_List[subdomain]
                
                # If the domain path has not been visited, add it and increment the count
                if not visited:
                    pgc.Subdomains_List[subdomain][domain_path] = 1
                    pgc.Unique['ICS_Subdomains'][full_subdomain] = pgc.Unique['ICS_Subdomains'].get(full_subdomain, 0) + 1

                # If the domain path has been visited, just increment the visit count
                else:
                    pgc.Subdomains_List[subdomain][domain_path] += 1
            
            # Update unique pages and link list
            pgc.Unique['Pages'] += 1 if link not in pgc.Link_List else 0
            pgc.Link_List[link] = pgc.Link_List.get(link, 0) + 1
        
        # Sort and update unique ICS subdomains
        pgc.Unique['ICS_Subdomains'] = dict(sorted(pgc.Unique['ICS_Subdomains'].items()))
        
        # Write updated page crawled information to JSON file
        write_json(PAGE_CRAWLED_PATH, pgc.__dict__)


    def is_similar(self, url: str, content: str) -> bool:
        self.visited_hashes = load_or_initialize_json(SIMHASH_PATH, {})
        if url in self.visited_hashes:
            current_hash = self.visited_hashes[url]
        else:
            current_hash = self.simhash.compute_simhash(content)
            self.visited_hashes[url] = current_hash
            write_json(SIMHASH_PATH, self.visited_hashes)

        temp_hashes = self.visited_hashes.copy()
        most_similar_url = None
        highest_similarity = 0

        for visited_url, visited_hash in temp_hashes.items():
            similarity_percent = self.simhash.similarity(current_hash, visited_hash)
            if visited_url != url:
                if similarity_percent >= SIMHASH_THRESHOLD:
                    print(f"\tSkipping, page is {similarity_percent*100}% similar to {visited_url}\n")
                    return True
                if similarity_percent > highest_similarity:
                    highest_similarity = similarity_percent
                    most_similar_url = visited_url

        if most_similar_url:
            print(f"\tMost similar page with {highest_similarity*100}% similarity is {most_similar_url}\n")
        return False