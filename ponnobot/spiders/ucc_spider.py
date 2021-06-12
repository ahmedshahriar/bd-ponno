import logging

import scrapy
from django.utils.text import slugify

from ponnobot.items import ProductItem
from products.models import Category


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
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        """
        :param **kwargs:
        :param response:
        :return: products and pagination callback
        """
        categories = response.css('div.breadcrumbs div.container ul.items li ::text').getall()[1:]
        tag_list = []
        if len(categories) > 1:
            tag_list = [slugify(value, allow_unicode=True) for value in categories[1:]]
        if 'others' in tag_list:  # filter 'other' tag
            tag_list.remove('others')
        """ parse products """
        product_page_links = response.css('div.product-hover  a')
        yield from response.follow_all(product_page_links, self.parse_product, meta={"category": categories[0].strip(),
                                                                                     "tag_list": [{"name": slugify(value, allow_unicode=True)} for
                                                                                                  value in tag_list]})

        """ parse test for a single product """
        # single_product_url = 'https://ucc-bd.com/msi-meg-z490-unify-motherboard.html'
        # single_product_url = 'https://ucc-bd.com/msi-b560m-pro-motherboard.html'
        # single_product_url = 'https://ucc-bd.com/transcend-ts32gjf880s-jetflash-880-32gb-otg-usb3-0-silver.html'
        # yield response.follow(single_product_url,
        #                       callback=self.parse_product)

        """ pagination """
        try:
            pagination_links = response.css('div.pages ul li a[title="Next"] ::attr("href")').get()
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
        category = response.request.meta['category']
        tag_list = response.request.meta['tag_list']

        if 'laptop' in category.lower():
            category = category.replace('Laptops', 'Laptop').title().strip()
        if 'monitor' in category.lower():
            category = category.replace('Monitors', 'Monitor').title().strip()

        item = ProductItem()
        category_obj = None
        try:
            item['vendor'] = self.name
            item['name'] = response.css('span[itemprop="name"] ::text').get()
            item['product_url'] = response.url
            item['tags'] = tag_list
            # product_details['category'] = response.css('ul.items li.item.category a ::text').get()
            try:
                item['in_stock'] = 1 if 'In' in response.css(
                    'div[title="Availability"] span ::text').get().strip() else 0
            except Exception as e:
                print(e, response.url)
            try:
                item['price'] = int(
                    float(response.css('meta[property="product:price:amount"] ::attr("content")').get().strip()))
            except Exception as e:
                print(e, response.url)

            item['image_url'] = response.css('img.lazyload.gallery-placeholder__image ::attr("data-src")').get()
        except Exception as e:
            print(e, response.url)
        if item['name'] is not None:

            try:
                category_obj = Category.objects.get(slug=slugify(category, allow_unicode=True))
                logging.info("category already exists")
            except Category.DoesNotExist:
                category_obj = Category(name=category, slug=slugify(category, allow_unicode=True))
                category_obj.save()

            print(item, category)
            product_item_new = item.save()

            # insert category object
            product_item_new.category.add(category_obj)
