import logging

import scrapy
from django.utils.text import slugify

from ponnobot.items import ProductItem
from products.models import Category


class MKElectronicsSpider(scrapy.Spider):
    name = "mke"
    allowed_domains = ['mke.com.bd']

    start_urls = ['https://www.mke.com.bd/televisions?p=1',
                  'https://www.mke.com.bd/air-conditioners',
                  'https://www.mke.com.bd/refrigerators-freezers',
                  'https://www.mke.com.bd/cooling-heating-appliances',
                  'https://www.mke.com.bd/wash-dry-cleaning-appliances',
                  'https://www.mke.com.bd/kitchen-appliances',
                  'https://www.mke.com.bd/audio-video',
                  'https://www.mke.com.bd/personal-care-appliances',
                  'https://www.mke.com.bd/water-treatment-appliances',
                  'https://www.mke.com.bd/small-household-appliances',
                  'https://www.mke.com.bd/accessories'
                  ]

    # start_urls = ['https://www.mke.com.bd/televisions']

    def parse(self, response, **kwargs):
        """
        :param response:
        :return: products and pagination callback
        """
        # todo : https://hexfox.com/p/how-to-filter-out-duplicate-urls-from-scrapys-start-urls/
        # global link

        """ parse products """
        # product_page_links = response.css('a.product-item-link ')
        # yield from response.follow_all(product_page_links, self.parse_product)

        """ parse test for a single product """
        single_product_url = 'https://www.mke.com.bd/samsung-ua78ks9000k-4k-curved-smart-tv'
        yield response.follow(single_product_url, callback=self.parse_product)

        """ pagination """
        # try:
        #     pagination_link = response.css('a[title="Next"] ::attr("href")').get()
        #     yield response.follow(pagination_link, self.parse)
        # except IndexError as ie:
        #     # logging.info(ie, logging.WARN)
        #     print(ie)
        # except TypeError as te:
        #     # logging.info(te, logging.WARN)
        #     print(te)
        # except ValueError as ve:
        #     print(ve)

    def parse_product(self, response):
        item = ProductItem()
        category_obj = None
        try:
            item['vendor'] = self.name
            item['product_url'] = response.url
            item['name'] = response.css('meta[property="og:title"] ::attr("content") ').get()
            item['image_url'] = response.css('meta[property="og:image"] ::attr("content") ').get()
            item['price'] = int(float(response.css('meta[property="product:price:amount"] ::attr("content") ').get()))
            item['in_stock'] = 1 if 'in' in response.css(
                'meta[property="product:availability"] ::attr("content") ').get().lower() else 0
            category = response.css('div.breadcrumbs ul.items li.item a ::text').getall()[-1]
            brand = response.css('meta[property="product:brand"] ::attr("content") ').get()
            color = response.css('meta[property="product:color"] ::attr("content") ').get()
            product_category = response.css('meta[property="product:category"] ::attr("content") ').get()
            item['tags'] = [{"name": value} for value in [brand, product_category, color] if value is not None]

            try:
                category_obj = Category.objects.get(slug=slugify(category, allow_unicode=True))
                logging.info("category already exists")
            except Category.DoesNotExist:
                category_obj = Category(name=category, slug=slugify(category, allow_unicode=True))
                category_obj.save()
        except Exception as e:
            print(e, response.url)
        if item['name'] is not None:
            print(category_obj, item)
            product_item_new = item.save()

            # insert category object
            product_item_new.category.add(category_obj)
