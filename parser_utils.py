import os
import ssl
import nltk

from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from urllib.parse import urlparse
from constants import STOP_WORDS


# Do this first, that'll do something eval() to "materialize" the LazyCorpusLoader
next(nltk.corpus.wordnet.all_synsets())


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

    # Remove stop words from the tokens
    re_tokens = [token for token in re_tokens if token not in STOP_WORDS]

    # Identify the base form of any verbs (pos="v") and lemmatize those tokens
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(w, pos="v") for w in re_tokens]
    
    # Remove single-character tokens
    return [token for token in tokens if len(token) != 1]



def parse_url(link):
    """
    Parse the URL and extract the domain, subdomain, and path.
    """
    parsed_url = urlparse(link)
    domain = parsed_url.netloc.split('.', 1)[1]
    subdomain = parsed_url.netloc.split('.', 1)[0]
    path = parsed_url.path
    return domain, subdomain, path



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