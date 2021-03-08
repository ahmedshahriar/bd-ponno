import unicodedata

import scrapy

from ponnobot.items import ProductItem


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
        # yield response.follow(single_product_url, callback=self.parse_product)

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
        item['name'] = response.css('div.summary-inner h1[itemprop="name"] ::text').get()
        item['image_url'] = response.css('meta[property="og:image"] ::attr("content")').get()
        item['price'] = response.css('meta[property="product:price:amount"] ::attr("content")').get()
        item['in_stock'] = False if response.css('p.stock.out-of-stock ::text').get() else True
        yield item
