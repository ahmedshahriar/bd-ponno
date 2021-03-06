import re

import scrapy

from ponnobot.items import ProductItem


class ComputerSourceSpider(scrapy.Spider):
    name = "source"
    allowed_domains = ['computersourcebd.com']

    # start_urls = ['https://www.computersourcebd.com/']
    def start_requests(self):
        url = 'https://www.computersourcebd.com/'
        yield scrapy.Request(url=url, callback=self.begin_parse)

    def begin_parse(self, response):
        urls = response.css('ul.categories_mega_menu > li > a ::attr("href")').getall()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        :param response:
        :return: products and pagination callback
        """

        """ parse products """
        product_page_links = response.css('div.single_product div.product_thumb a')
        yield from response.follow_all(product_page_links, self.parse_product)

    def parse_product(self, response):
        item = ProductItem()
        item['vendor'] = self.name
        item['name'] = response.css('div.product_d_right h1 ::text').get()
        item['product_url'] = response.url
        item['image_url'] = response.css('meta[property="og:image"] ::attr("content")').get()
        yield item
