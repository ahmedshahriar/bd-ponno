import json
import re
from urllib.parse import urljoin

import scrapy

from ponnobot.items import ProductItem


class DarazSpider(scrapy.Spider):
    name = "daraz"
    allowed_domains = ['daraz.com.bd']

    BASE_URL = 'https://www.daraz.com.bd'

    # HEADERS = {
    #     'authority': 'my.daraz.com.bd',
    #     'pragma': 'no-cache',
    #     'cache-control': 'no-cache',
    #     'dnt': '1',
    #     'origin': 'https://www.daraz.com.bd',
    #     'referer': 'https://www.daraz.com.bd/',
    #     'upgrade-insecure-requests': '1',
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    #     'accept': 'application/json, text/javascript',
    #     'accept-encoding': 'gzip, deflate, br',
    #     'content-type': 'application/x-www-form-urlencoded',
    #     'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    #     'sec-ch-ua-mobile': '?0',
    #     'sec-fetch-site': 'same-site',
    #     'sec-fetch-mode': 'cors',
    #     'sec-fetch-dest': 'empty',
    #     'accept-language': 'en-US,en;q=0.9,bn;q=0.8,hi;q=0.7',
    # }

    # HEADERS = {
    #     'authority': 'my.daraz.com.bd',
    #     'pragma': 'no-cache',
    #     'cache-control': 'no-cache',
    #     'dnt': '1',
    #     'upgrade-insecure-requests': '1',
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    #     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    #     'sec-fetch-site': 'none',
    #     'sec-fetch-mode': 'navigate',
    #     'sec-fetch-dest': 'document',
    #     'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    # }

    def start_requests(self):

        yield scrapy.Request(url=self.BASE_URL, callback=self.begin_parse)

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
        product_page_links = [urljoin(self.BASE_URL, product["thumbs"][0]['productUrl']) for product in product_list]
        yield from response.follow_all(product_page_links, self.parse_product)
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

    def parse_product(self, response):
        item = ProductItem()
        raw_product_data = re.compile(r'app.run\((.*)\);').search(response.text)
        product_json = json.loads(raw_product_data.group(1).strip())['data']['root']['fields']['skuInfos']['0']
        # print(product_json,type(product_json))
        # print(raw_product_data.group(1))
        try:
            item['vendor'] = self.name
            item['product_url'] = response.url
            item['name'] = product_json["dataLayer"]["pdt_name"]
            item['image_url'] = product_json["image"]
            item['price'] = int(float(product_json["price"]["salePrice"]["value"]))
            item['in_stock'] = True if product_json["stock"] > 0 else False

        except Exception as e:
            print(e, response.url)
        if item['name'] is not None:
            item.save()
