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
    "https://today.uci.edu/department/information_computer_sciences/calendar",
    "https://wics.ics.uci.edu/events/",
    "https://wics.ics.uci.edu/a/language.php",
    "https://wics.ics.uci.edu/language.php",
    "https://wics.ics.uci.edu/recover/initiate",
    "https://ngs.ics.uci.edu/blog/page",
    "https://ngs.ics.uci.edu/category",
    "https://ngs.ics.uci.edu/tag/",
    "https://ngs.ics.uci.edu/author/",
    "https://isg.ics.uci.edu/events",
    "https://www.ics.uci.edu/publications",
    "https://www.ics.uci.edu/?",
    "https://www.ics.uci.edu?",
    "https://www.informatics.uci.edu/page",
    "https://www.cs.uci.edu/events",
    "https://www.informatics.uci.edu/very-top-footer-menu-items/news/page",
    "https://cbcl.ics.uci.edu/wgEncodeBroadHistone",
    "http://computableplant.ics.uci.edu/alphasite/index-challenge.html",
    "https://wiki.ics.uci.edu/doku.php",
    "https://swiki.ics.uci.edu/doku.php",
    "https://evoke.ics.uci.edu/",
    "https://grape.ics.uci.edu/",
    "https://wics.ics.uci.edu/",
    "https://www.ics.uci.edu/doku.php",
    "https://intranet.ics.uci.edu/doku.php",
    "https://cbcl.ics.uci.edu/doku.php",
    "gitlab.ics.uci.edu"
}

ALPHANUMERIC = {
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", 
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"
    }

MAX_HTTP_BYTES_SIZE = 10000000  # 10MB