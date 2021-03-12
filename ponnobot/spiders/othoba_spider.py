import scrapy


class OthobaSpider(scrapy.Spider):
    name = "othoba"
    allowed_domains = ['othoba.com']

    # start_urls = ['https://www.othoba.com/electronics']

    def start_requests(self):
        url = 'https://www.othoba.com/'

        yield scrapy.Request(url=url, callback=self.begin_parse)

    def begin_parse(self, response):
        urls = response.css('ul li.lnkHeading a ::attr("href")').getall()
        print(len(urls), urls)