from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from ponnobot.spiders.ryans_spider import RyanComputersSpider


class Command(BaseCommand):
    help = "Release the RyansComputers Crawler"

    def handle(self, *args, **options):
        process = CrawlerProcess(get_project_settings())
        process.crawl(RyanComputersSpider)
        process.start()
