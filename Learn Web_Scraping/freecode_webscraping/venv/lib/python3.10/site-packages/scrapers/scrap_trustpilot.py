
from .tools.scraper_tools import ReviewScraper, clean_xpath_res, _aux_clean_number
import json
import re


class TrustpilotScraper(ReviewScraper):
    def __init__(self, url, company=""):
        # page_argument = "page"
        next_page_xpath = "//a[@name='pagination-button-next']/@href"
        company_name_xpath = "//span[@class='multi-size-header__big']//text()"
        super().__init__(url=url,
                        next_page_xpath=next_page_xpath,
                        company=company,
                        company_name_xpath=company_name_xpath)
    
    def _parse_review(self, review_block):
        info = dict()
        info["company"] = self.company
        xpath_id = ".//h2/a/@href"
        info["review_id"] = clean_xpath_res(review_block.xpath(xpath_id))
        xpath_rating = ".//div[contains(@class, 'reviewHeader']/@data-service-review-rating"
        info["rating_star"] = clean_xpath_res(review_block.xpath(xpath_rating))
        # xpath_date = ".//div[@class='review-content-header__dates']/script/text()"
        # info["date"] = json.loads(review_block.xpath(xpath_date)[0])["publishedDate"]
        # xpath_title = ".//h2//text()"
        # info["title"] = clean_xpath_res(review_block.xpath(xpath_title))
        # xpath_review = ".//p[contains(@class, 'tyography_body']//text()"
        # info["review"] = clean_xpath_res(review_block.xpath(xpath_review))
        xpath_customer_location = ".//div[contains(@class, 'consumer-information__location')]//text()"
        info["customer_location"] = clean_xpath_res(review_block.xpath(xpath_customer_location))
        xpath_n_reviews = ".//div[@class='consumer-information__review-count']//text()"
        info["n_reviews_customer_hide"] = clean_xpath_res(review_block.xpath(xpath_n_reviews))
        xpath_is_verified_info = ".//div[contains(@class , 'review-content-header__review-labels')]/script/text()"
        is_verified_info = review_block.xpath(xpath_is_verified_info)
        if len(is_verified_info) > 0:
            is_verified_info = json.loads(is_verified_info[0])
        else:
            is_verified_info = dict()
        info["is_verified"] = is_verified_info.get('isVerified', False)
        info["verification_source_hide"] = is_verified_info.get('verificationSource', "")
        info["review_source_hide"] = is_verified_info.get('reviewSourceName', "")
        info["verification_level_hide"] = is_verified_info.get('verificationLevel', "")
        xpath_reply_date = ".//script[@data-initial-state='review-reply-dates']//text()"
        reply_date_info = clean_xpath_res(review_block.xpath(xpath_reply_date))
        if reply_date_info:
            reply_date_info = json.loads(reply_date_info)
            info["reply_date_hide"] = reply_date_info["publishedDate"]
        else:
            info["reply_date_hide"] = ""
        xpath_reply_content = ".//div[@class='brand-company-reply__content']//text()"
        info["reply_content_hide"] = clean_xpath_res(review_block.xpath(xpath_reply_content))
        return info

    def _parse_review_script(self, script):
        info = dict()
        info["reviewId"] = script.get("id", "")
        info["language"] = script.get("language", "")
        info["company"] = self.company
        info["title"] = script.get("title", "")
        info["review"] = script.get("text", "")
        info["rating_star"] = script.get("rating", "")
        try:
            info["date"] = script.get("dates", dict()).get("publishedDate", "")
        except:
            info["date"] = ""

        try:
            consumer_info = script.get("consumer", dict())
            info["customer_location"] = consumer_info.get("countryCode", "")
            info["n_reviews_customer_hide"] = consumer_info.get("numberOfReviews", "")
        except:
            info["customer_location"] = ""
            info["n_reviews_customer_hide"] = ""

        try:
            verified_info = script.get("labels", dict()).get("verification", dict())
            info["is_verified"] = verified_info.get("isVerified", "")
            info["verification_source_hide"] = verified_info.get("verificationSource", "")
            info["review_source_hide"] = verified_info.get("reviewSourceName", "")
            info["verification_level_hide"] = verified_info.get("verificationLevel", "")
        except:
            info["is_verified"] = ""
            info["verification_source_hide"] = ""
            info["review_source_hide"] = ""
            info["verification_level_hide"] = ""

        try:
            reply_info = script.get("reply", dict())
            info["reply_text_hide"] = reply_info.get("message", "")
            info["reply_date_hide"] = reply_info.get("publishedDate", "")
        except:
            info["reply_text_hide"] = ""
            info["reply_date_hide"] = ""

        return info

    def clean_review(self, r):
        cleaned_r = r.copy()
        # cleaned_r["rating_star_cleaned_hide"] = _aux_clean_number(r["rating_star"])
        # cleaned_r["n_reviews_customer_cleaned_hide"] = _aux_clean_number(r["n_reviews_customer_hide"])
        cleaned_r["date_year_month_hide"] = cleaned_r["date"][:7]
        cleaned_r["reply_date_year_month_hide"] = cleaned_r["reply_date_hide"][:7]
        cleaned_r["text_cleaned_hide"] = f"{cleaned_r['title']} {cleaned_r['review']}"
        cleaned_r["text_cleaned_hide"] = cleaned_r["text_cleaned_hide"].replace("[^a-zA-Z#]", " ").lower()
        return cleaned_r

    # def _parse_page(self, page):
    # """ Old version"""
    #     info = list()
    #     reviews = page.xpath("//div[contains(@class , 'review-card')]")
    #     reviews_script = page.xpath("//script[@type='application/json']//text()")
    #     if reviews_script:
    #         reviews_script = reviews_script[0]
    #         reviews_info = json.loads(reviews_script)["props"]["pageProps"]["reviews"]
    #     else:
    #         reviews_info = [dict() for r in reviews]
    #     for r, r_info in zip(reviews, reviews_info):
    #         res = self._parse_review(r)
    #         res_info = self._parse_review_script(r_info)
    #         if res["rating_star"] != '#rating/desc/star0#':
    #             res["language"] = r_info.get("inLanguage", "Unknown")
    #             info.append(self.clean_review(res))
    #     return info

    def _parse_page(self, page):
        info = list()
        reviews_script = page.xpath("//script[@type='application/json']//text()")
        reviews_info = []
        if reviews_script:
            reviews_script = reviews_script[0]
            reviews_info = json.loads(reviews_script)["props"]["pageProps"]["reviews"]
        for review in reviews_info:
            res = self._parse_review_script(review)
            info.append(self.clean_review(res))
        return info


    def scrap_n_reviews(self):
        page_html = self._get_html(self.url)
        # xpath_n_reviews = "//h2[@class='header--inline']//text()"
        # n_reviews_str = re.sub("[^0-9]", "", page_html.xpath(xpath_n_reviews)[0])
        # self.n_reviews = int(n_reviews_str.replace(" ", "").replace(".", ""))
        n_xpath = "//script[@id='__NEXT_DATA__']//text()"
        script = page_html.xpath(n_xpath)[0]
        json_script = json.loads(script)
        self.n_reviews = json_script["props"]["pageProps"]["businessUnit"]["numberOfReviews"]


    def get_n_pages(self):
        n_pages = self.n_reviews // 20 + 1 # 20 reviews per page
        # Not optimised, it's the max # of pages, but often less
        return n_pages

    def is_last_page(self, page):
        return len(page.xpath("//a[@name='pagination-button-next']")) == 0


def scrap_reviews_trustpilot(url):
    tps = TrustpilotScraper(url)
    info = tps.scrap_website()
    return info
