# Constants for scrapy, websites to scrape

from src.utils import get_exec_time, get_todays_data_dir, get_exec_date

KEY_TERMS = ["election", "war", "economy"]
SCRAPY_URLS = ["https://www.theguardian.com/europe"]  # ["https://www.ft.com/", # issues with ft access and scrapy
SCRAPER_JSON_PATH = get_todays_data_dir(get_exec_date()) / f'scraper_output_{get_exec_time().strftime("%Y-%m-%d-%H")}.json'

