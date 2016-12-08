import difflib
import html2text
import re
from bs4 import BeautifulSoup
from sqlalchemy import and_

from lawa_scraper.db import get_session
from ..models import Webpage, Diff
from .. import settings
from ..config import *
from ..utils import *

Session = get_session(settings.MYSQL_CONNECTION)


class MainAnalyzer:
    def __init__(self):
        self.session = Session()

    def run(self):
        pages = self._get_pages()
        for n in range(len(pages) - 1):
            diff = self.get_diff_obj(pages[n], pages[n+1])
            if diff not in self.session:
                self.session.add(diff)
                self.session.commit()

    def _get_pages(self):
        pages = self.session.query(Webpage).filter(
            and_(Webpage.html != None, Webpage.path_label == TARGET_URL)). \
            order_by(Webpage.original_url)
        p_list = []
        for p in pages:
            p_list.append(p)
        return p_list

    def get_diff_obj(self, old, new):
        diff = self.session.query(Diff) \
            .filter_by(original_url=new.original_url) \
            .first()
        if not diff:
            diff = Diff(original_url=new.original_url)
        diff_text = self._make_diff(old, new)
        diff.date = translate_timestamp(new.original_url)
        diff.diff = diff_text
        diff.path_label = TARGET_URL
        diff.company = COMPANY
        if "$" in diff_text:
            diff.pricing = 1
        else:
            diff.pricing = 0
        if "free" in diff_text.lower():
            diff.free = 1
        else:
            diff.free = 0
        diff.add_lines = self._count_lines(diff_text, r"\+")
        diff.delete_lines = self._count_lines(diff_text, r"\-")
        diff.add_diff = self._get_category_lines(diff_text, r"\+")
        diff.delete_diff = self._get_category_lines(diff_text, r"\-")
        return diff

    def _make_diff(self, old, new):
        text_maker = html2text.HTML2Text()
        text_maker.ignore_images = True
        text_maker.ignore_links = True
        text_maker.skip_internal_links = True
        old_html = self._remove_wa_header(old.html)
        new_html = self._remove_wa_header(new.html)
        old_text = text_maker.handle(old_html).splitlines()
        new_text = text_maker.handle(new_html).splitlines()
        g = difflib.ndiff(old_text, new_text)
        result = []
        for i in g:
            if re.match(r"\+|\-", i) and not re.match(r"\+\s+$", i):
                result.append(i)
        return "\n".join(result)

    def _remove_wa_header(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        soup.find(id="wm-ipp").extract()
        return soup.prettify()

    def _count_lines(self, diff, reg):
        diff_lines = diff.splitlines()
        count = 0
        for l in diff_lines:
            if re.match(reg, l):
                count += 1
        return count

    def _get_category_lines(self, diff, reg):
        diff_lines = diff.splitlines()
        text_list = []
        for l in diff_lines:
            if re.match(reg, l):
                text_list.append(l)
        return "\n".join(text_list)
