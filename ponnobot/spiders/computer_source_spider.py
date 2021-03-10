import re
from pprint import pprint

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
        try:
            _, price = (
                re.findall(r'-?\d+\.?\d*', p.strip().replace(',', ''))[0] for p in
                response.css('span.new_price ::text').getall())
            item['price'] = int(float(price))
        except ValueError as ve:
            print(ve,'##############################################################################', response.url)
        item['in_stock'] = False if response.css('p.stock.out-of-stock ::text').get() else True
        # item.save()
        yield item
