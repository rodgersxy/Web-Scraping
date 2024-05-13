import scrapy
from scrapy.http import Request

class AudibleSpider(scrapy.Spider):
    name = "audible"
    allowed_domains = ["www.audible.com"]
    start_urls = ["https://www.audible.com/search"]

    def parse(self, response):
        product_container = response.xpath('//div[@class="adbl-impression-container "]//li[contains(@class, "productListItem")]')
        for product in product_container:
            book_title = product.xpath('.//h3[contains(@class, "bc-heading")]/a/text()').get()
            book_author = product.xpath('.//li[contains(@class, "authorLabel")]/span/a/text()').getall()
            book_length = product.xpath('.//li[contains(@class, "runtimeLabel")]/span/text()').get()
            yield {
                'title': book_title,
                'author': book_author,
                'length': book_length,
            }

        # Follow pagination links
        next_page = response.xpath('//a[contains(@class, "next-link")]/@href').get()
        if next_page:
            yield Request(response.urljoin(next_page), callback=self.parse)