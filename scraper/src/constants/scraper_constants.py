# Constants for scrapy, websites to scrape

from src.utils import get_exec_time, get_todays_data_dir, get_exec_date
import datetime

KEY_TERMS = ["election", "war", "economy"]
SCRAPY_URLS = ["https://www.theguardian.com/europe"]  # ["https://www.ft.com/",
SCRAPER_JSON_PATH = get_todays_data_dir(get_exec_date()) / f'scraper_output_{get_exec_time().strftime("%Y-%m-%d-%H")}.json'


# class ScraperJsonPaths:
#     """
#     Paths that depend on the execution date.
#     """

#     def __init__(self, today: datetime.date):
#         self.today = today
#         self.SCRAPER_JSON_PATH = (
#             get_todays_data_dir(today=self.today) / "xml_to_send_to_elering.xml"
#         )


