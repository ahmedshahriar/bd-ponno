import logging
import re

import scrapy
from django.utils.text import slugify

from ponnobot.items import ProductItem
from products.models import Category


class StarTechBDSpider(scrapy.Spider):
    name = "startech"
    allowed_domains = ['startech.com.bd']

    # start_urls = ['https://startech.com.bd']

    def start_requests(self):
        url = 'https://startech.com.bd'
        yield scrapy.Request(url=url, callback=self.begin_parse)

    def begin_parse(self, response):
        # https://www.w3schools.com/cssref/css_selectors.asp
        urls = response.css('ul.responsive-menu > li.has-child > a:first-child ::attr("href")').getall()
        # print(len(urls), urls)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def clean_text(self, raw_html):
        """
        :param raw_html: this will take raw html code
        :return: text without html tags
        """
        cleaner = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        return re.sub(cleaner, '', raw_html)

    def parse(self, response):
        """
        :param response:
        :return: products and pagination callback
        """
        # add if needed for thumbnail
        # for product_info in response.css('div.product-thumb'):
        #     img = product_info.css('div.img-holder a > img ::attr("src")').get()
        #     print(img)

        """ parse products """
        product_page_links = response.css('h4.product-name  a')
        yield from response.follow_all(product_page_links, self.parse_product)

        """ parse test for a single product """
        # single_product_url = 'https://www.startech.com.bd/logic-x1-14-inch-laptop-cooler'
        # single_product_url = 'https://www.startech.com.bd/chuwi-hi10-air-touch-tablet-and-notebook'
        # single_product_url ='https://www.startech.com.bd/huawei-matebook-d15-laptop'  # out of stock
        # single_product_url = 'https://www.startech.com.bd/optoma-s341'
        # single_product_url = 'https://www.startech.com.bd/kwg-vela-m1-pc-case'
        # yield response.follow(single_product_url, callback=self.parse_product)

        """ pagination """
        try:
            pagination_links = response.css('ul.pagination li a ::attr("href")').getall()[-1]
            yield response.follow(pagination_links, self.parse)
        except IndexError as ie:
            # logging.info(ie, logging.WARN)
            print(ie)
        except TypeError as te:
            # logging.info(te, logging.WARN)
            print(te)
        except ValueError as ve:
            print(ve)

        # different approach for pagination
        #
        # next_page = response.css('ul.pagination li a ::attr("href")').getall()[-1]
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response):
        """
        :param response:
        :return: product details dictionary
        """

        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        item = ProductItem()
        tag_list = []
        category_obj = None
        try:
            # todo nested category
            category_count = len(response.css('span[itemprop="name"] ::text').getall())
            if category_count > 1:
                category = response.css('span[itemprop="name"] ::text').get().strip()
                categories = response.css('span[itemprop="name"] ::text').getall()[1:-1]
                tag_list.extend([slugify(category, allow_unicode=True) for category in categories if 'All' not in category])
                if 'component' in category.lower():
                    category = category.replace('Component','PC Components').title().strip()

            else:
                category = "other"
            brand = response.css('meta[property="product:brand"] ::attr("content")').get().lower()
            if brand not in tag_list:
                tag_list.append(slugify(brand, allow_unicode=True))
            tags = [{"name": value} for value in tag_list]
            # item['category'] = response.css('span[itemprop="name"] ::text').get()
            # item['category'] = Category.objects.first()

            try:
                category_obj = Category.objects.get(slug=slugify(category, allow_unicode=True))
                logging.info("category already exists")
            except Category.DoesNotExist:
                category_obj = Category(name=category, slug=slugify(category, allow_unicode=True))
                category_obj.save()

            item['vendor'] = self.name
            item['name'] = extract_with_css('h1.product-name ::text')
            item['tags'] = tags
            item['product_url'] = response.url
            item['in_stock'] = 0 if 'Out' in response.css('td.product-status ::text').get() else 1
            item['price'] = int(float(response.css('meta[property="product:price:amount"] ::attr("content")')
                                      .get()))
            item['image_url'] = response.css('img.main-img ::attr("src")').get()

        except Exception as e:
            print(e, response.url)
        if item['name'] is not None:
            product_item_new = item.save()
            # print(item, category)

            # insert category object
            product_item_new.category.add(category_obj)
