
import re
import html
import json
from unidecode import unidecode
from .tools.scraper_tools import ReviewScraper, clean_xpath_res, _aux_clean_number


class TrustedshopsScraper(ReviewScraper):
    def __init__(self, url, company=""):
        page_argument = "page"
        company_name_xpath = "//span[@class='shop-name']//text()"

        super().__init__(url=url,
                        page_argument=page_argument,
                        company_name_xpath=company_name_xpath,
                        use_chrome=True,
                        )
    
    def _parse_review(self, review_block):
        info = dict()
        info["rating_star"] = review_block["reviewRating"]["ratingValue"]
        info["date_full_hide"] = review_block["datePublished"]
        info["date"] = review_block["datePublished"][:10]
        info["review"] = review_block["reviewBody"]
        info["language"] = review_block["inLanguage"]
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
        xpath_n_reviews = "//h2[@class='summary-info']/span[1]//text()"
        n_reviews_str = re.sub("[^0-9]", "", page_html.xpath(xpath_n_reviews)[0])
        self.n_reviews = int(n_reviews_str.replace(" ", "").replace(".", ""))
    
    def get_n_pages(self):
        n_pages = self.n_reviews // 20 + 1 # 20 reviews per page
        # Not optimised, it's the max # of pages, but often less
        return n_pages

    def is_last_page(self, page):
        return page.xpath("//div[@page-index='next']/@style") == ["display: none;"]


def scrap_reviews_trustedshops(url):
    tss = TrustedshopsScraper(url)
    info = tss.scrap_website()
    return info
