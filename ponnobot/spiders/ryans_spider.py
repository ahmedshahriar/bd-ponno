import logging
import unicodedata
import scrapy


class RyanComputersSpider(scrapy.Spider):
    name = "ryans"
    allowed_domains = ['ryanscomputers.com']
    start_urls = ['https://www.ryanscomputers.com/category/notebook-all-notebook']

    def parse(self, response):
        """
        :param response:
        :return: products and pagination callback
        """
        """ parse products """
        # product_page_links = response.css('div.product-thumb a ::attr("href")')
        # yield from response.follow_all(product_page_links, self.parse_product)

        """ parse test for a single product """
        single_product_url = 'https://www.ryanscomputers.com/avita-essential-intel-cdc-n4000-110ghz-260ghz-4gb-lpddr4-128gb-ssd-no-odd-14-inch-fhd-1920x1080-ips-display-win-10-s-matt-black-notebook'

        yield response.follow(single_product_url, callback=self.parse_product)

        """ pagination """
        # try:
        #     # pagination_links = response.css('div.pages ol li a[rel="next"] ::attr("href")').get()
        #     # yield response.follow(pagination_links, self.parse)
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
        product_details = dict()
        product_details['name'] = response.css('h1.title ::text').get()
        product_details['product_url'] = response.url
        product_details['old_price'] = unicodedata.normalize("NFKD",response.css('span.old-price ::text').get().strip())
        product_details['special_price'] = unicodedata.normalize("NFKD", response.css('div.special-price span.price ::text').get().strip())
        product_details['image'] = response.css('meta[property="og:image"] ::attr("content")').get().strip().replace('thumbnail','main')
        product_details['available'] = False if response.css('div.out-of-stock-wrapper') else True
        yield product_details
