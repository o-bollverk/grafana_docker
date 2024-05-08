from pathlib import Path
from src.constants.scraper_constants import SCRAPY_URLS, SCRAPER_JSON_PATH, KEY_TERMS
from src.constants.scraper_constants import SCRAPER_JSON_PATH
from src.utils import get_exec_time

import scrapy
import re
import datetime
import json
# import pandas as pd

class KeywordSpider(scrapy.Spider):
    name = "policy_scraper"
    

    def start_requests(self):
        # SCRAPY_URLS = [
        #     "https://quotes.toscrape.com/page/1/",
        #     "https://quotes.toscrape.com/page/2/",
        # ]
        # SCRAPY_URLS = [ "https://www.theguardian.com/europe"] # "https://www.ft.com/",
        #SCRAPY_URLS = [ "https://www.ft.com/"] # "",

        for url in SCRAPY_URLS:
            yield scrapy.Request(url=url, callback=self.parse)

    def collect(self, response):
        
        major_headings = response.css('.dcr-v1s16m::text').getall()
        subheadings = response.css("script.span::text").getall()
        all_headings = major_headings + subheadings 
        
        site = "theguardian"
        timestamp = get_exec_time().strftime("%Y-%m-%d %H:%M:%S")

        for key_term in KEY_TERMS:
            regex_pattern = r'\b{}\b'.format(re.escape(key_term))
            res_list = [len(re.findall(regex_pattern, x, re.IGNORECASE)) for x in all_headings]

            yield {
                "term": key_term,
                "incidence": sum(res_list),
                "site": site,
                "timestamp": timestamp,
            }

    def parse(self, response):

        #today = pd.Timestamp.now().strftime("%Y-%m-%d")
        #today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(SCRAPER_JSON_PATH,"w") as f:
            for element in self.collect(response):
                json.dump(element, f)
                f.write("\n")
