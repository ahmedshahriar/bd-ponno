from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from ponnobot.spiders.hirakraja_spider import HirakRajaSpider


class Command(BaseCommand):
    help = "Release the Hirakraja Crawler"

    def handle(self, *args, **options):
        process = CrawlerProcess(get_project_settings())
        process.crawl(HirakRajaSpider)
        process.start()
