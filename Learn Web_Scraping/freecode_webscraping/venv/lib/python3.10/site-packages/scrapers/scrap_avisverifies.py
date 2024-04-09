from .tools.scraper_tools import ReviewScraper, clean_xpath_res, _aux_clean_number
import re


class AvisVerifiesScraper(ReviewScraper):
    def __init__(self, url, company=""):
        page_argument = "p"
        company_name_xpath = "//span[@class='label-title']//span[@itemprop='name']//text()"
        super().__init__(url=url,
                        page_argument=page_argument,
                        company=company,
                        company_name_xpath=company_name_xpath)
    
    def _parse_review(self, review_block):
        info = dict()
        xpath_rating = ".//span[@itemprop='ratingValue']//text()"
        info["rating_star"] = clean_xpath_res(review_block.xpath(xpath_rating))
        xpath_date = ".//meta[@itemprop='datePublished']/@content"
        info["date"] = str(review_block.xpath(xpath_date)[0])
        xpath_review = ".//div[@itemprop='reviewBody']//text()"
        info["review"] = clean_xpath_res(review_block.xpath(xpath_review))
        xpath_details = ".//div[@class='details suite']//text()"
        info["details_hide"] = clean_xpath_res(review_block.xpath(xpath_details))
        xpath_answer = ".//div[@class='answers']/div[@class='merchant']//div[@class='text']//text()"
        info["answer"] = clean_xpath_res(review_block.xpath(xpath_answer))
        info["company_has_answered"] = len(info["answer"]) > 0
        return info

    def clean_review(self, r):
        cleaned_r = r.copy()
        cleaned_r["rating_star_cleaned_hide"] = _aux_clean_number(cleaned_r["rating_star"])
        cleaned_r["date_year_month_hide"] = f"{cleaned_r['date'][-4:]}-{cleaned_r['date'][3:5]}"
        cleaned_r["text_cleaned_hide"] = cleaned_r["review"].replace("[^a-zA-Z#]", " ").lower()

        return cleaned_r
        
    def _parse_page(self, page):
        info = list()
        reviews = page.xpath("//div[@class='review row']")
        for r in reviews:
            res = self._parse_review(r)
            info.append(self.clean_review(res))
        return info

    def scrap_n_reviews(self):
        page_html = self._get_html(self.url)
        xpath_n_reviews = "//span[@class='count']//text()"
        n_reviews_str = re.sub("[^0-9]", "", page_html.xpath(xpath_n_reviews)[0])
        self.n_reviews = int(n_reviews_str.replace(" ", ""))
    
    def get_n_pages(self):
        page_html = self._get_html(self.url)
        xpath_pages = "//select[@class='selectPage']/option"
        list_pages = page_html.xpath(xpath_pages)
        n_pages = len(list_pages)
        return n_pages

    def is_last_page(self, page):
        return len(page.xpath("//a[@rel='next']/@href")) == 0
    
    
def scrap_reviews_avisverifies(url):
    avs = AvisVerifiesScraper(url)
    info = avs.scrap_website()
    return info
