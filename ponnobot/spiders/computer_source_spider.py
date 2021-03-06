import re

import scrapy


class ComputerSourceSpider(scrapy.Spider):
    name = "source"
    allowed_domains = ['computersourcebd.com']

    # start_urls = ['https://www.computersourcebd.com/']
    def start_requests(self):
        url = 'https://www.computersourcebd.com/'
        yield scrapy.Request(url=url, callback=self.begin_parse)

    def begin_parse(self, response):
        urls = response.css('ul.categories_mega_menu > li > a ::attr("href")').getall()
        print(urls, len(urls))