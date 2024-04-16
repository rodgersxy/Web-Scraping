import sys
from lxml import html
import requests
from unidecode import unidecode
from time import sleep
from urllib.parse import (
        urljoin, urlencode, unquote, urlparse, parse_qsl, ParseResult
    )
from .generic_tools import logger, clean_xpath_res, _aux_clean_number
from .html_tools import get_html, current_page, next_url


class ReviewScraper:
    def __init__(self, url, page_argument=None, next_page_xpath="", 
                company="", company_name_xpath="",
                use_chrome=False, headless=True, force_new=False):
        self.url = url
        self.n_reviews = None
        self.reviews = []
        self.page_argument = page_argument
        self.next_page_xpath = next_page_xpath
        self.company = company
        self.company_name_xpath = company_name_xpath
        self.use_chrome = use_chrome
        self.headless = headless
        self.force_new = force_new
        self.company = self.get_company_name()

    def get_company_name(self):
        if self.company:
            return self.company
        if self.company_name_xpath:
            page_html = self._get_html(self.url)
            return clean_xpath_res(page_html.xpath(self.company_name_xpath))
        return ""
    
    def _get_html(self, url):
        return get_html(url, 
                        use_chrome=self.use_chrome, 
                        headless=self.headless, 
                        force_new=self.force_new)
    
    def _parse_review(self, review_block):
        return dict()

    def clean_review(self, review):
        return dict()

    def _parse_page(self, page):
        return []

    def scrap_n_reviews(self):
        return 0
    
    def get_n_pages(self):
        return 0

    def is_last_page(self, page):
        return True

    def _pause(self, n):
        if n % 1000 == 0:
            time_sleep = 25
        elif n % 100 == 0:
            time_sleep = 7
        elif n % 10 == 0:
            time_sleep = 1
        else:
            time_sleep = 0

        if self.n_reviews > 10000:
            time_sleep = 3 * time_sleep + 1
        elif self.n_reviews > 1000:
            time_sleep *= 2

        if time_sleep > 5:
            logger(f"Sleeping for {time_sleep}sec to avoid being blocked")
        if time_sleep:
            sleep(time_sleep)
    
    def scrap_reviews(self):
        print("Starting to scrap...")
        
        n_pages = self.get_n_pages()
        url = self.url
        n_start = current_page(url, self.page_argument)
        for n in range(n_start, n_pages + 1):
            page_html = self._get_html(url)
            page_info = self._parse_page(page_html)
            if len(page_info) == 0:
                break
            for i in page_info:
                i["page"] = n
                i["company"] = self.company
            self.reviews += page_info

            n_done = (n - n_start + 1)
            n_total = (n_pages - n_start + 1)
            percent_done = int( n_done / n_total * 100)

            display_msg = f"Done {n_done}/{n_total} ({percent_done}%): {url}"
            
            logger(display_msg)

            if self.is_last_page(page_html):
                break
            self._pause(n - n_start + 1)
            url = next_url(url, 
                            page_argument=self.page_argument,
                            page_html=page_html,
                            next_page_xpath=self.next_page_xpath)
    
    def scrap_website(self):
        self.scrap_n_reviews()
        self.scrap_reviews()
        res = {
        	"url": self.url,
        	"n_reviews": self.n_reviews,
        	"reviews": self.reviews
        }
        return res