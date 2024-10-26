# URL CONSTANTS
VALID_URLS = {
    ".ics.uci.edu", 
    ".cs.uci.edu", 
    ".informatics.uci.edu", 
    ".stat.uci.edu", 
    "today.uci.edu/department/information_computer_sciences/"
    }

BLACKLISTED_URLS = {
    "wics.ics.uci.edu/events/",
    "isg.ics.uci.edu/events/",
    "ics.uci.edu/events/",
    # "swiki.ics.uci.edu/doku.php/",
    # "grape.ics.uci.edu/wiki/asterix/",
    "ics.uci.edu/?",        # Trap: includes informatics.uci.edu and ics.uci.edu
    "ics.uci.edu?",         # More or less to avoid queries as well
    "gitlab.ics.uci.edu/"
    }



# WORDS
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



# SIZE CONSTANTS
MAX_HTTP_BYTES_SIZE = 10000000  # 10 MB Max for HTTP Response page
LOW_VALUE_SIZE = 15             # Equivalent to just around 1 sentence in a page


# PATH CONSTANTS
DATA_DIR = './data'
LINK_DUMP_PATH = f'{DATA_DIR}/link_dump.json'
PAGE_CRAWLED_PATH = f'{DATA_DIR}/page_crawled.json'
WORDS_STATS_PATH = f'{DATA_DIR}/words_stats.json'



# REGEX CONSTANTS
FILE_EXTENSIONS = (
    r".*\.(css|js|bmp|gif|jpe?g|ico"
    + r"|png|tiff?|mid|mp2|mp3|mp4"
    + r"|wav|avi|mov|mpg|mpeg|ram|m4v|mkv|ogg|ogv|pdf|bam|sam"
    + r"|ps|eps|tex|ppt|ppsx|pptx|doc|docx|xls|xlsx|names"
    + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
    + r"|epub|dll|cnf|tgz|sha1|odc|scm"
    + r"|thmx|mso|arff|rtf|jar|csv|apk"
    + r"|rm|smil|wmv|swf|wma|war|zip|rar|gz|z|zip)$"
)

PATH_SEGMENTS = {
    '/pdf/', '/doc/', '/uploads/', '/upload/', '/viewdoc/','/calendar/', '/events/', 
    '?do=', '?action=', '?from=', '?version=', '?rev=', '?idx=', '?share='
    }



# DATA STRUCTURE CONSTANTS
LINK_DUMP_STRUCTURE = {'Seed': {'Good': {}, 'Bad': {}}, 'Legal': {}, 'Removed': {}}
WORDS_STATS_STRUCTURE = {'Stats': {'Longest_Page_(words)': {}, '50_Most_Common_Words': {}}, 'URL_list': {},'Word_list': {}}
PAGES_CRAWLED_STRUCTURE = {'Unique': {'Pages': 0, 'ICS_Subdomains': {}}, 'Subdomains_List': {}, 'Link_List': {}}