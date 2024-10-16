import os
import json
import nltk

from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer

from urllib.parse import urlparse

from bs4 import BeautifulSoup
from constants import STOP_WORDS, MAX_HTTP_BYTES_SIZE



def check_status_code_correct_crawl(resp):
    """
    Check if the response status and content meet the criteria for a "correct crawl".

    This function ensures that:
    - The response status code is between 200 and 399.
    - The response contains data.
    - The response content size is less than the maximum allowed size.
    """
    ok_status = 200 <= resp.status <= 399
    has_data = resp.raw_response != None
    less_than_max_size = len(resp.raw_response.content) < MAX_HTTP_BYTES_SIZE if has_data else False

    return ok_status and has_data and less_than_max_size



def set_up_ssl():
    """
    Set up SSL context to allow unverified HTTPS connections.

    This function is used to bypass SSL verification, which is necessary
    for downloading NLTK data in some environments where SSL verification
    might fail.
    """
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context



def download_nltk_library():
    """
    Download the NLTK 'wordnet' library if it is not already present.

    This function sets up the NLTK data path and downloads the 'wordnet'
    corpus if it is not already available in the specified directory.

    Provides short definitions and usage examples, and records various semantic relations.
    Need to perform lemmatization.
    """
    nltk.data.path.append('./nltk_data/')
    if not os.path.exists('./nltk_data/corpora'):
        set_up_ssl()
        nltk.download('wordnet', download_dir='./nltk_data/')



def tokenize(text):
    """
    Tokenize and lemmatize the input text.

    This function uses NLTK's RegexpTokenizer to tokenize the text into words,
    converts them to lowercase, and then lemmatizes each word using WordNetLemmatizer.
    Single-character tokens are removed.

    We want to lemmatize the text for several reasons:
    - Helps in normalizing the text, for word frequency analysis, where you want to count all occurrences of a word regardless of its form.
    - Reduce the number of unique words in your dataset
    """
    re_tokenizer = RegexpTokenizer('[a-zA-Z0-9]+')
    re_tokens = re_tokenizer.tokenize(text.lower())
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(w, pos="v") for w in re_tokens]
    return [token for token in tokens if len(token) != 1]



def scrape_words(url, resp):
    """
    Scrape words from the response content and update word statistics.

    This function parses the HTML content of the response using BeautifulSoup,
    tokenizes and lemmatizes the text, removes stop words, and updates the
    word statistics stored in 'words_stats.json'. It also tracks the URL with
    the most words and the frequency of each word.
    """
    try:
        with open('./data/words_stats.json', 'r') as json_file:
            words_stats = json.load(json_file)
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        words_stats = {
            'Counter': {'Longest_Page_(words)': {}, '50_Most_Common_Words': {}},
            'URL_list': {}, 
            'Word_list': {}
        }

    download_nltk_library()
    soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
    text = soup.text
    token_list = tokenize(text)
    token_list_without_stopwords = [token for token in token_list if token not in STOP_WORDS]

    words_stats['URL_list'][url] = len(token_list)
    current_number_of_words = words_stats['Counter']['Longest_Page_(words)'].get(url, 0)
    if len(token_list) > current_number_of_words:
        words_stats['Counter']['Longest_Page_(words)'] = {url: len(token_list)}

    for token in token_list_without_stopwords:
        words_stats['Word_list'][token] = words_stats['Word_list'].get(token, 0) + 1

    sorted_words = sorted(words_stats['Word_list'].items(), key=lambda item: item[1], reverse=True)
    words_stats['Counter']['50_Most_Common_Words'] = dict(sorted_words[:50])

    with open('./data/words_stats.json', 'w') as json_file:
        json.dump(words_stats, json_file)



def get_page_crawled(link_list):
    """
    Update the list of crawled pages and their subdomains.

    This function reads the 'page_crawled.json' file to get the current list of
    crawled pages, updates it with the new links, and tracks the total number
    of unique pages and subdomains for 'ics.uci.edu'.
    """
    try:
        with open('./data/page_crawled.json', 'r') as json_file:
            page_crawled = json.load(json_file)
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        page_crawled = {
            'Counter': {'Unique_pages': 0, 'ics.uci.edu_subdomains': {}}
        }

    for link in link_list:
        parsed_url = urlparse(link)
        domain = parsed_url.netloc.split('.', 1)[1]
        subdomain = parsed_url.netloc.split('.', 1)[0]
        path = parsed_url.path

        if domain not in page_crawled:
            page_crawled[domain] = [{subdomain: [path]}]
            page_crawled['Counter']['Unique_pages'] += 1
            if domain == 'ics.uci.edu':
                page_crawled['Counter']['ics.uci.edu_subdomains'][subdomain] = 1
        else:
            subdomain_found = any(subdomain in nested_dict for nested_dict in page_crawled[domain])
            if not subdomain_found:
                page_crawled[domain].append({subdomain: [path]})
                page_crawled['Counter']['Unique_pages'] += 1
                if domain == 'ics.uci.edu':
                    page_crawled['Counter']['ics.uci.edu_subdomains'][subdomain] = 1
            else:
                for sub in page_crawled[domain]:
                    if subdomain in sub and path not in sub[subdomain]:
                        sub[subdomain].append(path)
                        page_crawled['Counter']['Unique_pages'] += 1
                        if domain == 'ics.uci.edu':
                            page_crawled['Counter']['ics.uci.edu_subdomains'][subdomain] += 1

    with open('./data/page_crawled.json', 'w') as json_file:
        json.dump(page_crawled, json_file)