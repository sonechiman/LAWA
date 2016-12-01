# -*- coding: utf-8 -*-

import os

BOT_NAME = 'lawa_scraper'

SPIDER_MODULES = ['lawa_scraper.spiders']
NEWSPIDER_MODULE = 'lawa_scraper.spiders'

COOKIES_ENABLED = False


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'lawa_scraper (+http://www.yourdomain.com)'

# ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'lawa_scraper.pipelines.MysqlWebpagePipeline': 100,
}

LOG_FILE = "lawa.log"

DOWNLOAD_DELAY = 3

MYSQL_CONNECTION = os.environ.get(
    'WEBARCHIVE_DATA_MYSQL',
    'mysql://root@localhost/webarhive'
)

try:
    import local_settings
    for var in dir(local_settings):
        vars()[var] = getattr(local_settings, var)
except ImportError:
    pass