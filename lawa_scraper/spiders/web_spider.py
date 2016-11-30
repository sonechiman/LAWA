# -*- coding: utf-8 -*-

import os
import scrapy
import re
from datetime import datetime as dt
from ..items import PageItem
from ..utils import *


class WebpageSpider(scrapy.Spider):
    name = 'webpage'
    allowed_domains = ['web.archive.org']

    def __init__(self, url=None, *args, **kwargs):
        super(WebpageSpider, self).__init__(*args, **kwargs)
        if not isinstance(url, list):
            url = [url]
        self.start_urls = url
        self.start_urls = ["http://web.archive.org/web/20000622002011/http://www.salesforce.com/"]

    def parse(self, response):
        page = PageItem()
        page["html"] = response.body
        page["original_url"] = response.url
        page["url"] = translate_url(response.url)
        page["timestamp"] = translate_timestamp(response.url)
        yield page
        # next_urls = response.css('#wm-ipp-inside .d a').xpath("@href").extract()
        # if next_urls:
        #     next_url = "http://web.archive.org" + next_urls[-1]
        #     yield scrapy.Request(url=next_url, callback=self.parse)
