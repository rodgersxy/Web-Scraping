
import re
import html
import json
from unidecode import unidecode
from .tools.scraper_tools import ReviewScraper, clean_xpath_res, _aux_clean_number
from .tools.html_tools import get_html
from .tools.generic_tools import logger

class IGraalScraper(ReviewScraper):
    def __init__(self, url, company=""):
        next_page_xpath = "//head/link[@rel='next']/@href"
        company_name_xpath = "//span[@class='shop-name']//text()"

        super().__init__(url=url,
                        next_page_xpath=next_page_xpath,
                        company_name_xpath=company_name_xpath,
                        use_chrome=True,
                        headless=False,
                        )
        print("A window will open. If a captcha is required, please fill it. \
Also close any popup that may appear.")

        get_html(url)
    
    def _parse_review(self, review_block):
        info = dict()
        info["rating_star"] = review_block["reviewRating"]["ratingValue"]
        info["date"] = review_block["datePublished"][:10]
        info["review"] = review_block["reviewBody"]
        return info

    def clean_review(self, r):
        cleaned_r = r.copy()
        cleaned_r["rating_star_cleaned_hide"] = r["rating_star"]
        cleaned_r["date_year_month_hide"] = cleaned_r["date"][:7]
        cleaned_r["text_cleaned_hide"] = unidecode(html.unescape(f"{cleaned_r['review']}"))
        cleaned_r["text_cleaned_hide"] = cleaned_r["text_cleaned_hide"].replace("[^a-zA-Z#]", " ").lower()
        return cleaned_r

    def _parse_page(self, page):
        info = list()
        script = page.xpath("//head/script[@type='application/ld+json']//text()")[0]
        reviews = json.loads(script)["review"]
        for r in reviews:
            res = self._parse_review(r)
            info.append(self.clean_review(res))
        return info

    def scrap_n_reviews(self):
        page_html = self._get_html(self.url)
        script = page_html.xpath("//head/script[@type='application/ld+json']//text()")[0]
        info = json.loads(script)
        self.n_reviews = info["aggregateRating"]["ratingCount"]
    
    def get_n_pages(self):
        n_pages = self.n_reviews // 50 + 1 # 50 reviews per page
        # Not optimised, it's the max # of pages, but often less
        return n_pages

    def is_last_page(self, page):
        return len(page.xpath(self.next_page_xpath)) == 0


def scrap_reviews_igraal(tss, url):
    # tss = IGraalScraper(url)
    info = tss.scrap_website()
    return info
