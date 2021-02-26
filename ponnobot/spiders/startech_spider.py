import re

import scrapy


class StarTechBDSpider(scrapy.Spider):
    name = "startech"
    allowed_domains = ['startech.com.bd']

    def start_requests(self):
        url = 'https://startech.com.bd'
        yield scrapy.Request(url=url, callback=self.begin_parse)

    def begin_parse(self, response):
        # https://www.w3schools.com/cssref/css_selectors.asp
        urls = response.css('ul.responsive-menu  li.has-child.c-1 > a:first-child ::attr("href")').getall()
        # print(len(urls),urls)
        for url in urls[:1]:
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

        product_details = dict()
        product_details['vendor'] = self.name
        product_details['name'] = extract_with_css('h1.product-name ::text')
        # todo nested category
        # product_details['category'] = response.css('span[itemprop="name"] ::text').getall()[:-1]
        product_details['category'] = response.css('span[itemprop="name"] ::text').get()
        product_details['product_url'] = response.url
        product_details['available'] = False if 'Out' in response.css('td.product-status ::text').get() else True
        product_attrs = response.css('td.product-info-label ::text').getall()
        product_attr_values = response.css('td.product-info-data ::text').getall()

        for key, value in zip(product_attrs, product_attr_values):
            if key == "Price":
                product_details['price'] = value
        product_details['image_url'] = response.css('img.main-img ::attr("src")').get()
        yield product_details
