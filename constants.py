VALID_URLS = {
    ".ics.uci.edu", 
    ".cs.uci.edu", 
    ".informatics.uci.edu", 
    ".stat.uci.edu", 
    "today.uci.edu/department/information_computer_sciences/"
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

BLACKLISTED_URLS = {
    "today.uci.edu/department/information_computer_sciences/calendar",
    "ics.uci.edu/events",
    "ngs.ics.uci.edu/blog/page",
    "ngs.ics.uci.edu/category",
    "ngs.ics.uci.edu/tag/",
    "ngs.ics.uci.edu/author/",
    "isg.ics.uci.edu/events",
    "ics.uci.edu/publications",
    "ics.uci.edu/?",
    "ics.uci.edu?",
    "informatics.uci.edu/page",
    "informatics.uci.edu/very-top-footer-menu-items/news/page",
    "cbcl.ics.uci.edu/wgEncodeBroadHistone",
    "computableplant.ics.uci.edu/alphasite/index-challenge.html",
    "evoke.ics.uci.edu",
    "grape.ics.uci.edu",
    "wics.ics.uci.edu/events/",
    "wics.ics.uci.edu/a/language.php",
    "wics.ics.uci.edu/language.php",
    "wics.ics.uci.edu/recover/initiate",
    "wics.ics.uci.edu",
    "ics.uci.edu/doku.php",
    "wiki.ics.uci.edu/doku.php",
    "swiki.ics.uci.edu/doku.php",
    "intranet.ics.uci.edu/doku.php",
    "cbcl.ics.uci.edu/doku.php",
    "gitlab.ics.uci.edu"
}

ALPHANUMERIC = {
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", 
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"
    }

MAX_HTTP_BYTES_SIZE = 10000000  # 10MB