# -*- coding: utf-8 -*-

from datetime import datetime as dt


def translate_url(url):
    url_list = url.strip("/").split("/")
    return "/".join(url_list[7:])


def translate_timestamp(url):
    url_list = url.strip("/").split("/")
    time_string = url_list[4]
    return dt.strptime(time_string, '%Y%m%d%H%M%S')


def get_crawl_url(path):
    return "http://web.archive.org" + path
