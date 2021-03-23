from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from ponnobot.spiders.daraz_spider import DarazSpider


class Command(BaseCommand):
    help = "Release the Mke Crawler"

    def handle(self, *args, **options):
        process = CrawlerProcess(get_project_settings())
        process.crawl(DarazSpider)
        process.start()
