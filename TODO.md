[x] Improve current implementation for requirement 4 (subdomains of uci.edu ordered alphabetically, and how many links each subdomain contains)

[x] need to remove queries from crawled urls - solved by splitting link string on question mark after defrag

[x] currently revisting websites

[x] Avoid revisiting crawled/scraped websites already

[x] Seed url downloads sometimes points to .pdf/etc... files instead of actual pages. Status code detects and minigates it but if one return 200 it will read it. Probably need to fix it for better run time

[x] Add more documentation in scraper.py

[x] Check if there's any OK links in Removed list in link_dump

[x] Fix unique pages count and subdomain count

[x] Fix Largest page is currently https://ics.uci.edu/~seal/projects/deldroid/ArchManager.apk which is not correct

[x] Some url has ' ' spaces in them, need to remove them

[x] (Not sure if this is the right call but) Want to fix reading in urls such as http://www.informatics.uci.edu/files/pdf/InformaticsBrochure-March2018 where its still a pdf file but re doesn't catch it. Are we supposed to read in pdf uploads? Bc some have paths like /pdf/, /doc/, /uploads/, so if not then we should fix this in is_valid()

[x] What are large files (in MB?), especially if they have low information value (?)

[x] Some url are not lowered cased: like DataGuard.ics.uci.edu, or DataProtector.ics.uci.edu, and it messes up the the alphabetical sort in our function

[x] I did this: two or more requests to the same domain, possibly from separate threads, must have a delay of 500ms. But probably if there was a way to actually check it that would be great

[x] Check if crawler fell into any traps

[x] Lemmatization doesn't play well with multithreading (or at least the way I implemented it, keeps throwing an error).

[x] Holy Interleaved multithreading implementation, I'm literally the goat AND IT OBEYS POLITENESS POLICY LETS GOOO

[x] Sometimes you'll see "Some characters could not be decoded, and were replaced with REPLACEMENT CHARACTER." Is this a problem?

- This isn't really a problem, but it's warning you that Python has trouble decoding the character. (usually chars that are not utf-8):
    - Python defaults to replacing the character with the REPLACEMENT CHARACTER, which is U+FFFD (the question mark).
    - This is likely un-meaningful content from the webpage. ✅**Already handled**✅ by `parser_utils.tokenize()` as it only considers alphanumeric characters from the webpage text. 
    - Likely happening *within* `parser_utils.tokenize()` as it unwraps the webpage text. If you don't want the warning to show up consider silencing it while tokenizing.

[ ] Need to compare Single-Thread vs Multi-Thread runs, and see if there are any discrepancy / diff

[ ] Extra credit: Implement exact and near webpage similarity detection using the methods discussed in the lecture. Your implementation must be made from scratch, no libraries are allowed.
