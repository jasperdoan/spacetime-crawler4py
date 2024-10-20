[x] Improve current implementation for requirement 4 (subdomains of uci.edu ordered alphabetically, and how many links each subdomain contains)

[x] need to remove queries from crawled urls - solved by splitting link string on question mark after defrag

[x] currently revisting websites

[x] Avoid revisiting crawled/scraped websites already

[x] Seed url downloads sometimes points to .pdf/etc... files instead of actual pages. Status code detects and minigates it but if one return 200 it will read it. Probably need to fix it for better run time

[x] Add more documentation in scraper.py

[x] Check if there's any OK links in Removed list in link_dump

[x] Fix unique pages count and subdomain count

[ ] Fix Largest page is currently https://ics.uci.edu/~seal/projects/deldroid/ArchManager.apk which is not correct

[ ] Check if crawler fell into any traps

[ ] What are large files (in MB?), especially if they have low information value (?)

[ ] Want to fix reading in urls such as http://www.informatics.uci.edu/files/pdf/InformaticsBrochure-March2018 where its still a pdf file but re doesn't catch it

