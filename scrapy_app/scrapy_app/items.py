# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyAppItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class TorSpiderItem(scrapy.Item):
    page = scrapy.Field()
    url = scrapy.Field()
    urls = scrapy.Field()
    date = scrapy.Field()
    domain = scrapy.Field()
    title = scrapy.Field()
    homepage = scrapy.Field()
    external_links_web = scrapy.Field()
    external_links_tor = scrapy.Field()
    scheme = scrapy.Field()
    version = scrapy.Field()
    response_header = scrapy.Field()
    rendered_page = scrapy.Field()
    raw_page = scrapy.Field()
    redirect = scrapy.Field()
