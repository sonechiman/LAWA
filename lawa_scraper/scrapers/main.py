import os
from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess
from scrapy import signals
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
import logging
from sqlalchemy import and_

from lawa_scraper.db import get_session
from ..models import Webpage
from ..spiders.url_spider import UrlSpider
from ..spiders.web_spider import WebpageSpider
from .. import settings
from ..config import *


Session = get_session(settings.MYSQL_CONNECTION)


class MainCrawler:
    def __init__(self):
        self.settings = get_project_settings()
        self.session = Session()

    def run(self, url=TARGET_URL):
        self.process = CrawlerProcess(self.settings)
        self.url = url
        self.flag = "top_urls"
        configure_logging()
        # self.crawl_url()
        self.crawl_top_pages()
        self.process.start()

    # Use repetedly
    def _crawl(self, spider, callback, urls=None):
        crawler = self.process.create_crawler(spider)
        crawler.signals.connect(callback, signal=signals.spider_closed)
        self.process.crawl(crawler, urls)

    def crawl_url(self, url=None):
        if not url:
            url = self.url
        spider = UrlSpider(url=url)
        self._crawl(spider, self.callbacks)

    def crawl_page(self, urls=None):
        logging.info(urls[0])
        spider = WebpageSpider(url=urls)
        self._crawl(spider, self.callbacks, urls)

    # Each functions
    def crawl_top_pages(self):
        logging.info("START CRAWLING TOP PAGES")
        self.flag = "top_pages"
        pages_q = self.session.query(Webpage.original_url).filter(
            and_(Webpage.html == None, Webpage.path_label == self.url))
        page_list = []
        for p in pages_q:
            page_list.append(p[0])
        self.crawl_page(page_list)

    # Callbacks
    def callbacks(self, spider=None, urls=None):
        logging.info("START CALLBACKS")
        if self.flag == "top_urls":
            self.crawl_top_pages()
        elif self.flag == "top_pages":
            reactor.stop()

if __name__ == "__main__":
    MainCrawler().run()
