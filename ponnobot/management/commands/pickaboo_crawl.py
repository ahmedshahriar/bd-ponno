from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from ponnobot.spiders.pickaboo_spider import PickabooSpider


class Command(BaseCommand):
    help = "Release the Pickaboo Crawler"

    def handle(self, *args, **options):
        process = CrawlerProcess(get_project_settings())
        process.crawl(PickabooSpider)
        process.start()
