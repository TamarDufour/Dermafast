# scraping
data was extracted from [דפי זהב](https://www.d.co.il/SearchResults?query=%D7%A7%D7%95%D7%A4%D7%95%D7%AA+%D7%97%D7%95%D7%9C%D7%99%D7%9D) search on "קופת חולים"

scraping was done using webscraper addon for firefox

**to reproduce data:**
1. install [web-scraper](https://webscraper.io/) on your browser 
2. import golden_pages.json as a sitemap
3. run scrape
4. export data as csv
5. run clean_data.py with the data in the folder
---
## cleaned data output
1. address - the address of the clinic
2. sniff_provider - the name of the healthcare provider for the clinc (maccabi \ clalit \ meuhedet \ leumit)
3. phone_num - phone number of the clinic
4. times - string of working hours and days
5. extra_info - information about what services are provided in the clinic (physiotherapy \ lab services \ etc)