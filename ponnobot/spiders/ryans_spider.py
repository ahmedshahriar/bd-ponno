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
        try:
            pagination_links = response.css('div.pages ol li a[rel="next"] ::attr("href")').get()
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
        product_details = dict()
        product_details['name'] = response.css('h1.title ::text').get()
        product_details['old_price'] = unicodedata.normalize("NFKD",response.css('span.old-price ::text').get().strip())
        product_details['special_price'] = unicodedata.normalize("NFKD", response.css('div.special-price span.price ::text').get().strip())

        # following sibling  : https://stackoverflow.com/questions/33904058/using-normalize-space-with-scrapy

        # normalize-space after following-sibling : https://www.reddit.com/r/scrapy/comments/epvkhy/xpath_use_of_sibling/

        # https://stackoverflow.com/questions/5992177/what-is-the-difference-between-normalize-space-and-normalize-spacetext

        # https://stackoverflow.com/questions/21118582/normalize-space-just-works-with-xpath-not-css-selector/46962320

        features = response.xpath('//p[contains(@class, "quick-overview-style")]/following-sibling::text()[normalize-space(.)]').getall()
        product_details['features'] = [specification_label.strip() for specification_label in features]
        # for info in response.css('div#information '):
        #     print(info.css('div.specs-item-wrapper ::text').getall())
        yield product_details
