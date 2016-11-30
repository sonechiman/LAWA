import os
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from retty_models import get_session
from retty_scraper import settings
from lawa_scraper.spiders.web_spider import WebpageSpider
from scrapy.utils.project import get_project_settings
import sys


class MainCrawler:
    def __init__(self):
        Session = get_session(settings.MYSQL_CONNECTION)
        self.settings = get_project_settings()
        self.session = Session()

    def run(self, url="http://web.archive.org/web/19991128155334/http://www.salesforce.com/"):
        self.url = url
        self.crawl_page()
        log.start()
        reactor.run()

    def _crawl(self, spider, callback):
        crawler = Crawler(self.settings)
        crawler.signals.connect(callback, signal=signals.spider_closed)
        crawler.configure()
        crawler.crawl(spider)
        crawler.start()

    def crawl_page(self):
        spider = WebpageSpider(url=self.url)
        self._crawl(spider, reactor.stop)

if __name__ == "__main__":
    MainCrawler().run()
