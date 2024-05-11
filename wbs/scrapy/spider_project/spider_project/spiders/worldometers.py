import scrapy
import random
import time
import json

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
        self.data = []

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
            country_data = {
                'country_name': country_name,
                'country_link': country_link,
                'population_data': []
            }
            self.data.append(country_data)

            # Follow the link to the individual country page
            country_url = response.urljoin(country_link)
            yield scrapy.Request(url=country_url, callback=self.parse_country, meta={'country_data': country_data}, headers={'User-Agent': random.choice(self.user_agent_list)})

    def parse_country(self, response):
        country_data = response.meta['country_data']
        rows = response.xpath("(//table[contains(@class,'table')])[1]/tbody/tr")
        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()
            country_data['population_data'].append({
                'year': year,
                'population': population
            })

    def closed(self, reason):
        with open('countries.json', 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)