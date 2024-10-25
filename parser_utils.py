import os
import ssl
import nltk

from nltk.tokenize import RegexpTokenizer
from urllib.parse import urlparse
from constants import STOP_WORDS


def tokenize(text):
    """
    Tokenize the input text.

    This function uses NLTK's RegexpTokenizer to tokenize the text into words,
    converts them to lowercase, and removes single-character tokens.

    We want to tokenize the text for several reasons:
    - Helps in normalizing the text, for word frequency analysis, where you want to count all occurrences of a word regardless of its form.
    - Reduce the number of unique words in your dataset
    """
    # Tokenize the text into words, re_tokens = ['word1', 'word2', ...]
    re_tokenizer = RegexpTokenizer('[a-zA-Z0-9]+')
    re_tokens = re_tokenizer.tokenize(text.lower())
    re_tokens = [token for token in re_tokens if token not in STOP_WORDS]
    
    # Remove single-character tokens
    return [token for token in re_tokens if len(token) != 1]



def parse_url(link):
    """
    Parse the URL and extract the domain, subdomain, and path.
    """
    parsed_url = urlparse(link)
    domain = parsed_url.netloc.split('.', 1)[1]
    subdomain = parsed_url.netloc.split('.', 1)[0]
    path = parsed_url.path
    return domain, subdomain, path