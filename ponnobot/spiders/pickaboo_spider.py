import logging

import scrapy
from django.utils.text import slugify

from ponnobot.items import ProductItem
from products.models import Category


class PickabooSpider(scrapy.Spider):
    name = "pickaboo"
    allowed_domains = ['pickaboo.com']

    # start_urls = ['https://pickaboo.com']
    # start_urls = ['https://www.pickaboo.com/electronics-appliances/television.html']

    def start_requests(self):
        url = 'https://www.pickaboo.com'

        yield scrapy.Request(url=url, callback=self.begin_parse)

    def begin_parse(self, response):
        urls = response.css('ul.em-menu-content > li ul li a ::attr("href")').getall()
        # print(len(urls), urls)
        url = None
        try:
            for url in urls:
                print(url)
                yield scrapy.Request(url=url, callback=self.parse)
        except Exception as e:
            print(e, url)

    def parse(self, response, **kwargs):
        """
        :param response:
        :return: products and pagination callback
        """
        """ parse product list """

        categories = response.css('div.breadcrumbs ul.items > li > * ::text').getall()[1:]
        tag_list = []
        if len(categories) > 1:
            tag_list = [slugify(value, allow_unicode=True) for value in categories[1:]]
        if 'others' in tag_list:  # filter 'other' tag
            tag_list.remove('others')

        product_page_links = response.css('li.product-item div  a ')
        yield from response.follow_all(product_page_links, self.parse_product, meta={"category": categories[0].strip(),"tag_list":[{"name": value} for value in tag_list]})

        # single_product_url = "https://www.pickaboo.com/sony-bravia-w66f-50-led-full-hd-high-dynamic-range-hdr-smart-tv.html"
        # "https://www.pickaboo.com/electronics-appliances/kitchen-appliance/others.html"

        # print(tag_list, categories[0].strip())
        # yield response.follow(single_product_url, callback=self.parse_product, meta={"category": categories[0].strip(),"tag_list":tag_list})

        """ pagination """
        try:
            pagination_links = response.css('div.pages ul li.pages-item-next a ::attr("href")').get()
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
        """
        :param response:
        :return: product details dictionary
        """
        category = response.request.meta['category']
        # print('################', category)
        tag_list = response.request.meta['tag_list']
        item = ProductItem()
        category_obj = None
        try:
            item['vendor'] = self.name
            item['name'] = response.css('meta[name="title"] ::attr("content")').get().strip()
            item['tags'] = tag_list
            item['product_url'] = response.url
            item['in_stock'] = 1 if response.css('.product-info-stock-sku div.stock.available') else 0
            item['price'] = int(float(response.css('meta[property="product:price:amount"] ::attr("content")').get().strip()))
            item['image_url'] = response.css('meta[property="og:image"] ::attr("content")').get().strip()
            # stock check https://www.pickaboo.com/sony-bravia-w66f-50-led-full-hd-high-dynamic-range-hdr-smart-tv.html

            try:
                category_obj = Category.objects.get(slug=slugify(category, allow_unicode=True))
                logging.info("category already exists")
            except Category.DoesNotExist:
                category_obj = Category(name=category, slug=slugify(category, allow_unicode=True))
                category_obj.save()

        except Exception as e:
            print(e, response.url)
        if item['name'] is not None:
            product_item_new = item.save()

            # insert category object
            product_item_new.category.add(category_obj)
