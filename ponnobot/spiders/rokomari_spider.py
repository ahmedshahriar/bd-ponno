import scrapy

from ponnobot.items import ProductItem


class RokomariBookSpider(scrapy.Spider):
    name = "rokomari"
    allowed_domains = ['rokomari.com']
    start_urls = ['https://www.rokomari.com']

    # def start_requests(self):
    #     url = 'https://www.rokomari.com/book/categories'
    #     yield scrapy.Request(url=url, callback=self.begin_parse)
    #
    # def begin_parse(self, response):
    #     urls = response.css('div.pFIrstCatCaroItem a ::attr("href")').getall()
    #     print(len(urls), urls)
    #     for url in urls[1:]:
    #         url = 'https://www.rokomari.com' + str(url)
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        """
        :param response:
        :return: products and pagination callback
        """
        """ parse products """

        # product_page_links = response.css('div.book-list-wrapper div.home-details-btn-wrapper  a ')
        # yield from response.follow_all(product_page_links, self.parse_product)

        """ parse test for a single product """
        single_product_url = 'https://www.rokomari.com/book/132098/a-mind-for-numbers'
        yield response.follow(single_product_url,
                              callback=self.parse_product)

        """ pagination """
        try:
            pagination_links = response.css('div.pagination a ::attr("href")').getall()[-1]
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
        tag_list = []
        category_obj = None

        item['vendor'] = self.name
        item['product_url'] = response.url
        item['name'] = response.css('div.details-book-main-info__header h1 ::text').get().strip()
        item['price'] = int(
            float(response.css('meta[property="product:price:amount"] ::attr("content")').get().strip()))
        item['in_stock'] = 0 if 'in' in response.css(
            'meta[property="product:availability"] ::attr("content")').get().strip().lower() else 1
        item['image_url'] = response.css('meta[property="og:image"] ::attr("content")').get().strip()
        publisher = response.css('td.publisher-link a ::text').get().strip()
        # todo check for brand name in bangla
        # response.css('meta[property="product:brand"] ::attr("content")').get().strip()

        tag_list.append(publisher)
        category = response.css('div.details-book-info__content-category a.ml-2 ::text').get().strip()
        author_name = response.css('p.details-book-info__content-author a ::text').get().strip()
        tag_list.append(author_name)
        print(category, item, tag_list)

