# -*- coding: utf-8 -*-

# from lawa_scraper.scrapers import main
from lawa_scraper.analysis import main
import logging

if __name__ == "__main__":
    try:
        # main.MainCrawler().run()
        main.MainAnalyzer().run()
    except Exception as e:
        logging.log(logging.CRITICAL, "ERROR HANDLING")
        logging.log(logging.CRITICAL, str(e))
