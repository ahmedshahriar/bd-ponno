import json
import logging

import scrapy
from django.utils.text import slugify

from ponnobot.items import ProductItem
from products.models import Category


class HirakRajaSpider(scrapy.Spider):
    name = "hirakraja"
    allowed_domains = ['hirakraja.com']

    # start_urls = ['https://hirakraja.com']

    def start_requests(self):
        url = 'https://hirakraja.com'

        yield scrapy.Request(url=url, callback=self.begin_parse)

    def begin_parse(self, response):
        # check source code
        # urls = response.css('div#amegamenu > ul.anav-top > li.amenu-item > div.adropdown > div.aitem a ::attr("href")').getall()
        urls = response.css('div.category-tree ul li a ::attr("href")').getall()
        # print(urls)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):

        """ parse products """
        product_page_links = response.css('div.product-list div.product-thumbnail a')
        yield from response.follow_all(product_page_links, self.parse_product)

        """ pagination """
        try:
            pagination_link = response.css('ul.page-list li a[rel="next"] ::attr("href")').get()
            if pagination_link:
                yield response.follow(pagination_link, self.parse)
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
        tag_list = []
        category_obj, category = None, None
        try:
            product_json = json.loads(response.css('div#product-details ::attr("data-product")').get())
            item['vendor'] = self.name
            item['name'] = product_json['name']
            item['price'] = product_json['price_amount']
            item['product_url'] = response.url

            # category = product_json['category_name'].strip()
            categories = response.css('ol.breadcrumb li span[itemprop="name"] ::text').getall()[1:]
            # todo : check category  https://hirakraja.com/home/2256-t20-installation-free-foldable-motorized-treadmill.html
            category = categories[0]
            if len(categories) > 1:
                tag_list.extend([category for category in categories[1:-1] if 'All' not in category])
                item['tags'] = [{"name": slugify(value, allow_unicode=True)} for value in tag_list]

            item['image_url'] = product_json['images'][0]['bySize']['medium_default']['url']
            item['in_stock'] = 1 if product_json['availability'].strip().lower() == "available" or  "last_remaining_items" else 0
        except Exception as e:
            print(e, response.url)

        if item['name'] is not None:
            try:
                category_obj = Category.objects.get(slug=slugify(category, allow_unicode=True))
                logging.info("category already exists")
            except Category.DoesNotExist:
                category_obj = Category(name=category, slug=slugify(category, allow_unicode=True))
                category_obj.save()

            # print(item, category)
            product_item_new = item.save()

            # insert category object
            product_item_new.category.add(category_obj)
