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
        print(len(urls))
