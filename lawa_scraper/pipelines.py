# -*- coding: utf-8 -*-

from .models import Webpage
from .db import get_session
from .items import PageItem
from . import settings

Session = get_session(settings.MYSQL_CONNECTION)


class MysqlPipeline(object):
    item_class = None

    def __init__(self):
        self.session = Session()

    def process_item(self, item, spider):
        if isinstance(item, self.__class__.item_class):
            self._process_item(item, spider)
            self.session.commit()
        return item

    def _process_item(self, item, spider):
        pass

    def _set_attributes(self, db_item, item):
        for k, v in item.items():
            if v is not None:
                if v == u"-":
                    v = None
                setattr(db_item, k, v)


class MysqlWebpagePipeline(MysqlPipeline):
    item_class = PageItem

    def _process_item(self, item, spider):
        page = self.session.query(Webpage) \
            .filter_by(original_url=item['original_url']) \
            .first()

        if not page:
            page = Webpage(original_url=item['original_url'])

        self._set_attributes(page, item)
        if page not in self.session:
            self.session.add(page)
