# -*- coding: utf-8 -*-

from .db import Base
from sqlalchemy import Column, String, DateTime, Text, Integer


class Webpage(Base):
    __tablename__ = 'web_pages'

    id = Column(Integer, primary_key=True)
    html = Column(Text)
    url = Column(String, nullable=False)
    original_url = Column(String, nullable=False, index=True, unique=True)
    company = Column(String, nullable=False, index=True)
    path_label = Column(String, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)

    def __repr__(self):
        return "<Webpage(id={0}, company={1}, timestamp={2})>".format(
            self.id, self.company, self.timestamp)
