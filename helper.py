from bs4 import BeautifulSoup
from constants import STOP_WORDS, MAX_HTTP_BYTES_SIZE
from json_utils import load_or_initialize_json, write_json
from parser_utils import set_up_ssl, download_nltk_library, tokenize, parse_url


class Helper:

    def check_status_code_correct_crawl(self, resp):
        """
        Check if the response status and content meet the criteria for a "correct crawl".

        This function ensures that:
        - The response status code is between 200 and 399.
        - The response contains data.
        - The response content size is less than the maximum allowed size.
        """
        # Check resp status between 2xx:Success & 3xx:Redirection
        ok_status = 200 <= resp.status <= 399

        # Check if the response has data
        has_data = resp.raw_response != None 
                                                       
        # Check if the response content size is less than MAX_HTTP_BYTES_SIZE
        less_than_max_size = len(resp.raw_response.content) < MAX_HTTP_BYTES_SIZE if has_data else False

        return ok_status and has_data and less_than_max_size



    def scrape_words(self, url, resp):
        """
        Scrape words from the response content and update word statistics.

        This function parses the HTML content of the response using BeautifulSoup,
        tokenizes and lemmatizes the text, removes stop words, and updates the
        word statistics stored in 'words_stats.json'. It also tracks the URL with
        the most words and the frequency of each word.
        """
        # Load/Init the 'words_stats.json' file
        words_stats = load_or_initialize_json(
            './data/words_stats.json', 
            {
                'Stats': {
                    'Longest_Page_(words)': {}, 
                    '50_Most_Common_Words': {}
                    }, 
                'URL_list': {},
                'Word_list': {}})
        
        # Download the NLTK 'wordnet' library if it is not already present
        # Parse and extract data from HTML tags using BeautifulSoup
        download_nltk_library()
        soup = BeautifulSoup(resp.raw_response.content, 'html.parser')

        # Tokenize the text from the soup(HTML content) + Lemmatize the tokens + Remove stop words
        token_list = tokenize(soup.text)
        token_list = [token for token in token_list if token not in STOP_WORDS]

        # Save {URL:Number of words/tokens} in 'words_stats.json'
        words_stats['URL_list'][url] = len(token_list)

        # Update the frequency of each word in the token list
        for token in token_list:
            words_stats['Word_list'][token] = words_stats['Word_list'].get(token, 0) + 1

        # Sort the URL_list by the number of words in descending order and update the longest page
        sorted_url_list = sorted(words_stats['URL_list'].items(), key=lambda item: item[1], reverse=True)
        words_stats['Stats']['Longest_Page_(words)'] = {sorted_url_list[0][0]: sorted_url_list[0][1]}

        # Sort the word list by frequency and save the 50 most common words
        sorted_words = sorted(words_stats['Word_list'].items(), key=lambda item: item[1], reverse=True)
        words_stats['Stats']['50_Most_Common_Words'] = dict(sorted_words[:50])

        # Save the all statistics to 'words_stats.json'
        write_json('./data/words_stats.json', words_stats)



    def get_page_crawled(self, link_list):
        """
        Update the list of crawled pages and their subdomains.

        This function reads the 'page_crawled.json' file to get the current list of
        crawled pages, updates it with the new links, and tracks the total number
        of unique pages and subdomains for 'ics.uci.edu'.
        """
        # Init/Update the 'page_crawled.json' file with the new links
        page_crawled = load_or_initialize_json(
            './data/page_crawled.json', 
            {
                'Stats': {
                    'Unique_Pages': 0, 
                    'ICS_Subdomains': {}},
                'Full_Link_Lists':{}})

        for link in link_list:
            domain, subdomain, path = parse_url(link)

            if domain == 'ics.uci.edu' and subdomain != 'www':
                page_crawled['Stats']['ICS_Subdomains'][f'{subdomain}.{domain}'] = page_crawled['Stats']['ICS_Subdomains'].get(subdomain, 0) + 1

            if link not in page_crawled['Full_Link_Lists']:
                page_crawled['Full_Link_Lists'][link] = 1
                page_crawled['Stats']['Unique_Pages'] += 1

        
        write_json('./data/page_crawled.json', page_crawled)