# -*- coding: utf-8 -*-

import os
import scrapy
import re
from datetime import datetime as dt
from ..items import PageItem
from ..utils import *


class UrlSpider(scrapy.Spider):
    name = 'url'
    allowed_domains = ['web.archive.org']

    def __init__(self, url=None, *args, **kwargs):
        super(UrlSpider, self).__init__(*args, **kwargs)
        target_url = "http://salesforce.com/"
        self.start_urls = self.get_start_urls(target_url)
        # self.start_urls = ["https://web.archive.org/web/20160701000000*/http://salesforce.com/"]

    def parse(self, response):
        path_list = response.css("#wbCalendar .pop li a").xpath("@href").extract()
        for path in path_list:
            yield self.parse_url(get_crawl_url(path))

        # next_urls = response.css("#wbChartThis a").xpath("@href").extract()[1:]
        # for url in next_urls:
        #     next_url = get_crawl_url(url)
        #     yield scrapy.Request(url=next_url, callback=self.parse)

    def parse_url(self, url):
        page = PageItem()
        page["original_url"] = url
        page["url"] = translate_url(url)
        page["timestamp"] = translate_timestamp(url)
        return page

    def get_start_urls(self, target_url):
        start_urls = []
        for y in range(1999, 2016):
            path = "/web/%s0301000000*/%s" % (y, target_url)
            start_urls.append(get_crawl_url(path))
        return start_urls
