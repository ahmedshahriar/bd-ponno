import logging
import re

import scrapy


class UCCSpider(scrapy.Spider):
    name = "ucc"
    allowed_domains = ['ucc-bd.com']
    # start_urls = ['https://ucc-bd.com/pc-components.html']

    def start_requests(self):
        url = 'https://ucc-bd.com/'
        yield scrapy.Request(url=url, callback=self.begin_parse)

    def begin_parse(self, response):
        # https://www.w3schools.com/cssref/css_selectors.asp
        urls = response.css('div.block-vmagicmenu-content ul.nav-desktop li.level1.category-item > a:first-child '
                            '::attr("href")').getall()
        # print(len(urls),urls)
        for url in urls[:1]:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        """
        :param response:
        :return: products and pagination callback
        """

        """ parse products """
        product_page_links = response.css('div.product-hover  a')
        yield from response.follow_all(product_page_links, self.parse_product)

        """ parse test for a single product """
        # single_product_url = 'https://ucc-bd.com/msi-meg-z490-unify-motherboard.html'
        # yield response.follow(single_product_url,
        #                       callback=self.parse_product)

        """ pagination """
        # try:
        #     pagination_links = response.css('div.pages ul li a[title="Next"] ::attr("href")').get()
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
        product_details = dict()
        product_details['vendor'] = self.name
        product_details['name'] = response.css('span[itemprop="name"] ::text').get()
        product_details['product_url'] = response.url
        product_details['category'] = response.css('ul.items li.item.category a ::text').get()
        product_details['available'] = response.css('div[title="Availability"] span ::text').get()
        product_details['price'] = response.css('meta[property="product:price:amount"] ::attr("content") ').get()
        product_details['image_url'] = response.css('img.lazyload.gallery-placeholder__image ::attr("data-src")').get()
        yield product_details
