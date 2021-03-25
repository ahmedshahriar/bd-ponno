import json
import re

import scrapy


class DarazSpider(scrapy.Spider):
    name = "daraz"
    allowed_domains = ['daraz.com.bd']

    def start_requests(self):
        url = 'https://www.daraz.com.bd'

        yield scrapy.Request(url=url, callback=self.begin_parse)

    def begin_parse(self, response):
        urls = response.css('ul.lzd-site-menu-sub li.lzd-site-menu-sub-item > a::attr("href")').getall()
        for url in urls:
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
        for product in product_list:
            yield product

        """ pagination """
        try:
            pagination_links = response.css('link[rel="next"] ::attr("href")').get()
            yield response.follow(pagination_links, self.parse)
        except IndexError as ie:
            # logging.info(ie, logging.WARN)
            print(ie)
        except TypeError as te:
            # logging.info(te, logging.WARN)
            print(te)
        except ValueError as ve:
            print(ve)