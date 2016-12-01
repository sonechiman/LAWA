# -*- coding: utf-8 -*-

import os
import scrapy
import re
from datetime import datetime as dt
import logging
from ..items import PageItem
from ..utils import *
from ..config import *


class WebpageSpider(scrapy.Spider):
    name = 'webpage'
    allowed_domains = ['web.archive.org']

    def __init__(self, url=None, *args, **kwargs):
        logging.info("START CRAWLING Web page spider")
        super(WebpageSpider, self).__init__(*args, **kwargs)
        if not isinstance(url, list):
            url = [url]
        self.start_urls = url

    def parse(self, response):
        page = PageItem()
        page["html"] = response.body
        page = self._parse_url(page, response.url)
        yield page

        link_list = response.css('a').xpath("@href").extract()
        paths = []

        # TODO: Refactoring
        for i in link_list:
            # For relative path (ex: index.html)
            if not re.search(r"(web|http|#|\*|javascript)", i) and i:
                paths.append(response.urljoin(i))
            if re.search(DOMAIN, i):
                paths.append(response.urljoin(i))
        for p in paths:
            url_list = response.url.strip("/").split("/")
            original_url = "/".join(url_list[:5])+"/"
            if re.match(original_url, p):
                next_page = PageItem()
                next_page["company"] = COMPANY
                temp_url = response.urljoin(p)
                next_page = self._parse_url(next_page, temp_url)
                yield next_page

    def _parse_url(self, page, url):
        page["original_url"] = url
        page["url"] = translate_url(url)
        page["timestamp"] = translate_timestamp(url)
        return page
