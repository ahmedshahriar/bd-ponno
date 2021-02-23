import logging
import unicodedata
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
        for url in urls:
            url = 'https://startech.com.bd' + str(url)
            print(url)
            # yield scrapy.Request(url=url, callback=self.parse)