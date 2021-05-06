import re

import scrapy

from ponnobot.items import ProductItem


class ComputerSourceSpider(scrapy.Spider):
    name = "source"
    allowed_domains = ['computersourcebd.com']

    start_urls = ['https://www.computersourcebd.com']
    # def start_requests(self):
    #     url = 'https://www.computersourcebd.com/'
    #     yield scrapy.Request(url=url, callback=self.begin_parse)
    #
    # def begin_parse(self, response):
    #     urls = response.css('ul.categories_mega_menu > li > a ::attr("href")').getall()
    #     print(urls, len(urls))
    #     # for url in urls:
    #     #     print(url)
    #     #     yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        """
        :param response:
        :return: products and pagination callback
        """

        """ parse products """
        # product_page_links = response.css('div.single_product div.product_thumb a')
        product_page_links = [
            'https://computersourcebd.com/product/1238/dell-vostro-14-3401-core-i3-10th-gen-14-inch-hd-laptop'
        # 'https://computersourcebd.com/product/206/apacer-ah25b-16gb-usb-31-pen-drive-',
        # 'https://computersourcebd.com/product/221/apacer-sdhc-uhs-1-16gb-class10-micro-sd-card',
        # 'https://computersourcebd.com/product/234/epson-l130-ink-tank-printer'
        # 'https://computersourcebd.com/product/536/apple-airpods'  # stock issue
        ]
        yield from response.follow_all(product_page_links, self.parse_product)

    def parse_product(self, response):
        item = ProductItem()

        item['vendor'] = self.name
        item['name'] = response.css('div.product_d_right h1 ::text').get()
        item['product_url'] = response.url
        item['image_url'] = response.css('meta[property="og:image"] ::attr("content")').get()
        category = response.css('div.breadcrumb_content div.breadcrumb_header a ::text').getall()[-1]
        if 'brand' in category.lower():
            category = category.replace('Brand','').title().strip()
        try:
            price = [re.findall(r'-?\d+\.?\d*', p.strip().replace(',', ''))[0] for p in
                     response.css('span.new_price ::text').getall()][-1]
            item['price'] = int(float(price))
        except ValueError as ve:
            print(ve, response.url)
        except IndexError as ie:
            print(ie, response.url)
        try:
            stock_status = response.css('div.product_d_right > p:last-of-type ::text').get()

            if stock_status is None:
                item['in_stock'] = True
            else:
                if 'Out' in stock_status:
                    item['in_stock'] = False
        except ValueError as ve:
            print(ve, response.url)
        # if item['name'] is not None:
        #     item.save()
        print(item, category)
