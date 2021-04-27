import logging

import scrapy
from django.utils.text import slugify

from ponnobot.items import ProductItem
from products.models import Category


class OthobaSpider(scrapy.Spider):
    name = "othoba"
    allowed_domains = ['othoba.com']

    start_urls = ['https://www.othoba.com/electronics']

    # def start_requests(self):
    #     url = 'https://www.othoba.com/'
    #
    #     yield scrapy.Request(url=url, callback=self.begin_parse)
    #
    # def begin_parse(self, response):
    #     urls = response.css('ul li.lnkHeading a ::attr("href")').getall()
    #     # print(len(urls), urls)
    #     for url in urls[:1]:
    #         url = 'https://www.othoba.com' + str(url)
    #         # print(url, sep='\n')
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        """
        :param response:
        :return: products and pagination callback
        """

        # todo sold out products from thumbnail
        """ parse products """
        # product_page_links = response.css('div.product-item > div.picture  a ')
        # yield from response.follow_all(product_page_links, self.parse_product)

        """ parse test for a single product """
        single_product_url = 'https://www.othoba.com/moveable-luxurious-garden-umbrella-60-aku00055' #stock issue
        yield response.follow(single_product_url, callback=self.parse_product)

        """ pagination """
        # try:
        #     pagination_links = response.css('div.pager ul li.next-page a ::attr("href")').get()
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
        """
        :param response:
        :return: product details dictionary
        """
        tag_list = []
        item = ProductItem()
        try:
            item['vendor'] = self.name
            item['product_url'] = response.url
            item['name'] = response.css('h1[itemprop="name"] ::text').get().strip()
            item['image_url'] = response.css('meta[property="og:image"] ::attr("content") ').get()
            item['price'] = int(float(response.css('div.product-price span ::attr("content")').get()))
            item['in_stock'] = False if response.css('span.sold-out').get() else True
            categories = response.css('div.breadcrumb a span ::text').getall()[1:]
            if len(categories) > 3:
                tag_list.extend([slugify(category, allow_unicode=True) for category in categories[:]])
            category_obj = None
            # try:
            #     category_obj = Category.objects.get(slug=slugify(categories[2], allow_unicode=True))
            #     logging.info("category already exists")
            # except Category.DoesNotExist:
            #     category_obj = Category(name=categories[1], slug=slugify(categories[2], allow_unicode=True))
            #     category_obj.save()
            item['tags'] = [{"name": value} for value in tag_list]
        except Exception as e:
            print(e, response.url)
        if item['name'] is not None:
            # item.save()
            print(item, categories)