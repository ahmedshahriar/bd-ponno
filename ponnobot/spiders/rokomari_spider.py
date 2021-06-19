import logging

import scrapy
from django.utils.text import slugify

from ponnobot.items import ProductItem
from products.models import Category


class RokomariBookSpider(scrapy.Spider):
    name = "rokomari"
    allowed_domains = ['rokomari.com']

    # start_urls = ['https://www.rokomari.com']

    def start_requests(self):
        url = 'https://www.rokomari.com/book/categories'
        yield scrapy.Request(url=url, callback=self.begin_parse)

    def begin_parse(self, response):
        urls = response.css('div.pFIrstCatCaroItem a ::attr("href")').getall()

        # print(len(urls), urls)
        for url in urls:
            url = 'https://www.rokomari.com' + str(url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        """
        :param response:
        :return: products and pagination callback
        """
        """ parse products """

        product_page_links = response.css('div.book-list-wrapper div.home-details-btn-wrapper  a ')
        yield from response.follow_all(product_page_links, self.parse_product)

        """ parse test for a single product """
        # single_product_url = 'https://www.rokomari.com/book/132098/a-mind-for-numbers'
        # yield response.follow(single_product_url,
        #                       callback=self.parse_product)

        """ pagination """
        try:
            pagination_links = response.css('div.pagination a ::attr("href")').getall()[-1]
            yield response.follow_all(pagination_links, self.parse)
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
        tag_list = []
        category_obj = None

        try:
            item['vendor'] = self.name
            item['product_url'] = response.url
            item['name'] = response.css('div.details-book-main-info__header h1 ::text').get().strip()
            item['price'] = int(
                float(response.css('meta[property="product:price:amount"] ::attr("content")').get().strip()))
            item['in_stock'] = 1 if 'in' in response.css(
                'meta[property="product:availability"] ::attr("content")').get().strip().lower() else 0
            item['image_url'] = response.css('meta[property="og:image"] ::attr("content")').get().strip()
            publisher = response.css('td.publisher-link a ::text').get().strip()
            # todo check for brand name in bangla
            # response.css('meta[property="product:brand"] ::attr("content")').get().strip()
            book_category = response.css('div.details-book-info__content-category a.ml-2 ::text').get().strip()

            category = 'Book'
            try:
                category_obj = Category.objects.get(slug=slugify(category, allow_unicode=True))
                logging.info("category already exists")
            except Category.DoesNotExist:
                category_obj = Category(name=category, slug=slugify(category, allow_unicode=True))
                category_obj.save()

            author_name = response.css('p.details-book-info__content-author a ::text').get().strip()
            tag_list.extend([publisher, author_name, book_category])
            item['tags'] = [{"name": slugify(value, allow_unicode=True)} for value in tag_list]

        except Exception as e:
            print(e, response.url)
        if item['name'] is not None:
            print(category_obj, item, tag_list)
            product_item_new = item.save()

            # insert category object
            product_item_new.category.add(category_obj)
