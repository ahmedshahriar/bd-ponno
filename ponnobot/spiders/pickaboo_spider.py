import scrapy


class PickabooSpider(scrapy.Spider):
    name = "pickaboo"
    allowed_domains = ['pickaboo.com']

    def start_requests(self):
        url = 'https://www.pickaboo.com'

        yield scrapy.Request(url=url, callback=self.begin_parse)

    def begin_parse(self, response):
        urls = response.css('ul.em-menu-content > li a ::attr("href")').getall()
        print(len(urls), urls)
        url = None
        try:
            for url in urls:
                print(url)
                yield scrapy.Request(url=url, callback=self.parse)
        except Exception as e:
            print(e, url)

    def parse(self, response, **kwargs):
        """
        :param response:
        :return: products and pagination callback
        """
        """ parse products """
        product_page_links = response.css('li.product-item div  a ')
        yield from response.follow_all(product_page_links)

        # single_product_url = "https://www.pickaboo.com/sony-bravia-w66f-50-led-full-hd-high-dynamic-range-hdr-smart-tv.html"
        #
        # yield response.follow(single_product_url, callback=self.parse_product)

        """ pagination """
        try:
            pagination_links = response.css('div.pages ul li.pages-item-next a ::attr("href")').get()
            yield response.follow(pagination_links, self.parse)
        except IndexError as ie:
            # logging.info(ie, logging.WARN)
            print(ie)
        except TypeError as te:
            # logging.info(te, logging.WARN)
            print(te)
        except ValueError as ve:
            print(ve)


