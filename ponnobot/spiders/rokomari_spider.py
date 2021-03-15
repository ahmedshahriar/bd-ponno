import scrapy


class RokomariBookSpider(scrapy.Spider):
    name = "rokomari"
    allowed_domains = ['rokomari.com']

    # start_urls = ['pFIrstCatCaroItem']

    def start_requests(self):
        url = 'https://www.rokomari.com/book/categories'
        yield scrapy.Request(url=url, callback=self.begin_parse)

    def begin_parse(self, response):
        urls = response.css('div.pFIrstCatCaroItem a ::attr("href")').getall()[:2]
        print(len(urls),urls)

        for url in urls[1:]:
            url = 'https://www.rokomari.com' + str(url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        """
        :param response:
        :return: products and pagination callback
        """
        """ parse products """

        # product_page_links = response.css('div.home-details-btn-wrapper  a ')
        # yield from response.follow_all(product_page_links, self.parse_product)

        """ parse test for a single product """
        single_product_url = 'https://www.rokomari.com/book/132098/a-mind-for-numbers'
        yield response.follow(single_product_url)