VALID_URLS = {
    ".ics.uci.edu", 
    ".cs.uci.edu", 
    ".informatics.uci.edu", 
    ".stat.uci.edu", 
    "today.uci.edu/department/information_computer_sciences/"
    }

BLACKLISTED_URLS = {
    "wics.ics.uci.edu/events/",
    "wics.ics.uci.edu/category/news/",
    "ngs.ics.uci.edu/blog/page",
    "ngs.ics.uci.edu/category",
    "ngs.ics.uci.edu/tag/",
    "ngs.ics.uci.edu/author/",
    "isg.ics.uci.edu/events",
    "ics.uci.edu/?",
    "ics.uci.edu?",
    "ics.uci.edu/events",
    "evoke.ics.uci.edu",
    "grape.ics.uci.edu",
    "wiki.ics.uci.edu",
    "swiki.ics.uci.edu",
    "intranet.ics.uci.edu",
    "cbcl.ics.uci.edu",
    "gitlab.ics.uci.edu"
    }

STOP_WORDS = {
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 
    "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 
    'but', 'by', 'can', "can't", 'cannot', 'com', 'could', "couldn't", 'did', "didn't", 'do',
    'does', "doesn't", 'doing', "don't", 'down', 'during', 'each', 'else', 'ever', 'few', 'for', 
    'from', 'further', 'get', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having', 'he', 
    'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'm", 
    'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself', "let's", 'me', 'more', 'most', 
    "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 
    'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', "shan't", 'she', "she'd", 
    "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's", 'the',
    'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they',
    "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under',
    'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were',
    "weren't", 'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while',
    'who', "who's", 'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't", 'you',
    "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves'
    }

MAX_HTTP_BYTES_SIZE = 5000000  # 5 MB

DATA_DIR = './data'
LINK_DUMP_PATH = f'{DATA_DIR}/link_dump.json'
PAGE_CRAWLED_PATH = f'{DATA_DIR}/page_crawled.json'
WORDS_STATS_PATH = f'{DATA_DIR}/words_stats.json'