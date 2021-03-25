import json
import re
from urllib.parse import urljoin

import scrapy


class DarazSpider(scrapy.Spider):
    name = "daraz"
    allowed_domains = ['daraz.com.bd']

    BASE_URL = 'https://www.daraz.com.bd'

    def start_requests(self):

        yield scrapy.Request(url=self.BASE_URL, callback=self.begin_parse)

    def begin_parse(self, response):
        urls = response.css('ul.lzd-site-menu-sub li.lzd-site-menu-sub-item > a::attr("href")').getall()
        for url in urls[:1]:
            url = "https:" + str(url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        """
        :param response:
        :return: products and pagination callback
        """
        """ parse products """

        raw_product_list = re.compile(r'window.pageData=(.*)</script>').search(response.text)
        product_list = json.loads(raw_product_list.group(1).strip())['mods']['listItems']
        product_page_links = [urljoin(self.BASE_URL, product["thumbs"][0]['productUrl']) for product in product_list]
        yield from response.follow_all(product_page_links[:1], self.parse_product)
        """ pagination """
        # try:
        #     pagination_links = response.css('link[rel="next"] ::attr("href")').get()
        #     yield response.follow(pagination_links, self.parse)
        # except IndexError as ie:
        #     # logging.info(ie, logging.WARN)
        #     print(ie)
        # except TypeError as te:
        #     # logging.info(te, logging.WARN)
        #     print(te)
        # except ValueError as ve:
        #     print(ve)

    def parse_product(self, response):
        # item = {}
        raw_product_data = re.compile(r'app.run\((.*)\);').search(response.text)
        print(json.loads(raw_product_data.group(1).strip())['data']['root']['fields']['skuInfos']['0'])
        # print(raw_product_data.group(1))
        # try:
        #     item['vendor'] = self.name
        #     # item['product_url'] = response.url
        #
        # except Exception as e:
        #     print(e, response.url)
        # if item['vendor'] is not None:
        #     yield item
