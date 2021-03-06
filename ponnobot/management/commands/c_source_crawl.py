from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from ponnobot.spiders.computer_source_spider import ComputerSourceSpider


class Command(BaseCommand):
    help = "Release the Computer Source BD Crawler"

    def handle(self, *args, **options):
        process = CrawlerProcess(get_project_settings())
        process.crawl(ComputerSourceSpider)
        process.start()
