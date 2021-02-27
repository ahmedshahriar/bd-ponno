from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from ponnobot.spiders.ucc_spider import UCCSpider


class Command(BaseCommand):
    help = "Release the Startech Crawler"

    def handle(self, *args, **options):
        process = CrawlerProcess(get_project_settings())
        process.crawl(UCCSpider)
        process.start()
