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