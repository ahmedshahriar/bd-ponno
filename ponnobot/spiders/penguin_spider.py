import logging
import unicodedata

import scrapy
from django.utils.text import slugify

from ponnobot.items import ProductItem
from products.models import Category


class PenguinBDSpider(scrapy.Spider):
    name = "penguin"
    allowed_domains = ['penguin.com.bd']
    start_urls = ['https://www.penguin.com.bd/product-category/health-care-essentials',
                  # 'https://www.penguin.com.bd/product-category/smart-home',
                  # 'https://www.penguin.com.bd/product-category/audio',
                  # 'https://www.penguin.com.bd/product-category/wearables',
                  # 'https://www.penguin.com.bd/product-category/charging-accessories',
                  # 'https://www.penguin.com.bd/product-category/mobile',
                  # 'https://www.penguin.com.bd/product-category/computers',
                  # 'https://www.penguin.com.bd/product-category/electronics'
                  ]

    def parse(self, response, **kwargs):
        """
        :param response:
        :return: products and pagination callback
        """
        """ parse products """
        product_page_links = response.css('div.product-element-top > a:first-child ::attr("href")')
        yield from response.follow_all(product_page_links, self.parse_product)

        """ parse test for a single product """
        # single_product_url = 'https://www.penguin.com.bd/product/d-link-dir-615x1-n300-300mbps-wireless-router/'
        # single_product_url = 'https://www.penguin.com.bd/product/brilliant-kn95-disposable-stereo-protective-face-mask-2pcs/'
        # single_product_url = 'https://www.penguin.com.bd/product/anker-soundcore-life-q10-hi-res-wireless-headphones-black/'
        single_product_url = 'https://www.penguin.com.bd/product/xiaomi-mijia-air-wear-anti-haze-face-mask/' # price issue
        yield response.follow(single_product_url, callback=self.parse_product)

        """ pagination """
        try:
            pagination_links = response.css(
                'nav.woocommerce-pagination ul.page-numbers li a.next.page-numbers ::attr("href")').get()
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
        item = ProductItem()

        item['vendor'] = self.name
        item['product_url'] = response.url
        item['name'] = response.css('div.summary-inner h1[itemprop="name"] ::text').get().strip()
        item['image_url'] = response.css('meta[property="og:image"] ::attr("content")').get()
        brand = response.css('div.woodmart-product-brand a img ::attr("title")').get()
        category = response.css('nav.woocommerce-breadcrumb a.breadcrumb-link ::text').getall()[1]

        # category_obj = None
        # try:
        #     category_obj = Category.objects.get(name=category)
        #     logging.info("category already exists")
        # except Category.DoesNotExist:
        #     category_obj = Category(name=category, slug=slugify(category, allow_unicode=True))
        #     category_obj.save()
        item['tags'] = [{"name": brand}] if brand else ""
        try:
            price = response.css('meta[property="product:price:amount"] ::attr("content")').get()

            if price is None:
                price = response.css('div.summary-inner p.price bdi::text').getall()[-1].replace(',', '')
            item['price'] = int(float(price))
        except ValueError as ve:
            print(ve, response.url)
        item['in_stock'] = 0 if response.css('p.stock.out-of-stock ::text').get() else 1
        print(item,category)
        # yield item
        # item.save()
        # product_item_new = item.save()
        #
        # # insert category object
        # product_item_new.category.add(category_obj)
