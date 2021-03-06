# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PageItem(scrapy.Item):
    html = scrapy.Field()
    timestamp = scrapy.Field()
    url = scrapy.Field()
    original_url = scrapy.Field()
    company = scrapy.Field()
    path_label = scrapy.Field()
