import scrapy

from ponnobot.items import ProductItem


class OthobaSpider(scrapy.Spider):
    name = "othoba"
    allowed_domains = ['othoba.com']

    # start_urls = ['https://www.othoba.com/electronics']

    def start_requests(self):
        url = 'https://www.othoba.com/'

        yield scrapy.Request(url=url, callback=self.begin_parse)

    def begin_parse(self, response):
        urls = response.css('ul li.lnkHeading a ::attr("href")').getall()
        # print(len(urls),urls)
        for url in urls:
            url = 'https://www.othoba.com' + str(url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        """
        :param response:
        :return: products and pagination callback
        """
        """ parse products """
        product_page_links = response.css('div.product-item div  a ')
        yield from response.follow_all(product_page_links, self.parse_product)

        """ pagination """
        try:
            pagination_links = response.css('div.pager ul li.next-page a ::attr("href")').get()
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
        item['name'] = response.css('h1[itemprop="name"] ::text').get().strip()
        item['price'] = response.css('div.product-price span ::attr("content")').get()
        item['brand'] = response.css('div.manufacturers span[itemprop="name"] a ::text').get()
        item['sku'] = response.css('div.sku span[itemprop="sku"] ::text').get()
        item['seller'] = response.css('div.product-vendor span.value a ::text').get()
        yield item
