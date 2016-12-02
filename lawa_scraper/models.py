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


class Diff(Base):
    __tablename__ = 'diff'

    id = Column(Integer, primary_key=True)
    diff = Column(Text, nullable=False)
    original_url = Column(String, nullable=False, index=True, unique=True)
    path_label = Column(String, index=True, nullable=False)
    company = Column(String, nullable=False, index=True)
    date = Column(DateTime, nullable=False, index=True)
    delete_lines = Column(Integer)
    add_lines = Column(Integer)
    princing = Column(Integer)
    free = Column(Integer)

    def __repr__(self):
        return "<Diff(id={0}, company={1}, timestamp={2})>".format(
            self.id, self.company, self.date)
