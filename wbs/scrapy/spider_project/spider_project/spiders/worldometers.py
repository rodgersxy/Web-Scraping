import scrapy
import random
import time
import csv

class WorldometersSpider(scrapy.Spider):
    name = "worldometers"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/world-population/population-by-country"]

    # List of user-agent strings to rotate
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    ]

    def __init__(self):
        self.csv_file = open('countries.csv', 'w', newline='', encoding='utf-8')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['Country Name', 'Country Link'])

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers={'User-Agent': random.choice(self.user_agent_list)})

    def parse(self, response):
        # Introduce a random delay between requests
        time.sleep(random.uniform(0.5, 1.5))

        # Check if there are pagination links
        next_page = response.xpath('//a[contains(text(), "Next")]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse, headers={'User-Agent': random.choice(self.user_agent_list)})

        # Extract country names and links
        countries = response.xpath('//td/a')
        for country in countries:
            country_name = country.xpath(".//text()").get()
            country_link = country.xpath(".//@href").get()
            self.csv_writer.writerow([country_name, country_link])

    def closed(self, reason):
        self.csv_file.close()