import difflib
import html2text
import re

from sqlalchemy import and_
from lawa_scraper.db import get_session
from ..models import Webpage
from .. import settings
from ..config import *

Session = get_session(settings.MYSQL_CONNECTION)


class MainAnalyzer:
    def __init__(self):
        self.session = Session()

    def run(self):
        pages = self._get_pages()
        print(pages[5].original_url)
        print(pages[6].original_url)
        print(self.make_diff(pages[6], pages[7]))

    def _get_pages(self):
        pages = self.session.query(Webpage).filter(
            and_(Webpage.html != None, Webpage.path_label == TARGET_URL)). \
            order_by(Webpage.original_url)
        p_list = []
        for p in pages:
            p_list.append(p)
        return p_list

    def make_diff(self, old, new):
        text_maker = html2text.HTML2Text()
        text_maker.ignore_images = True
        text_maker.ignore_links = True
        text_maker.skip_internal_links = True
        old_text = text_maker.handle(old.html).splitlines()
        new_text = text_maker.handle(new.html).splitlines()
        g = difflib.ndiff(old_text, new_text)
        result = []
        for i in g:
            if re.match(r"\+|\-", i):
                result.append(i)
        return "\n".join(result)
