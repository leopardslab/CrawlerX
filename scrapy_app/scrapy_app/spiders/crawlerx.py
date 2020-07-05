# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CrawlerxSpider(CrawlSpider):
    name = 'crawlerx'

    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]

        CrawlerxSpider.rules = [
            Rule(LinkExtractor(unique=True), callback='parse_item'),
        ]
        super(CrawlerxSpider, self).__init__(*args, **kwargs)

    def parse_item(self, response):
        # You can tweak each crawled page here
        # Don't forget to return an object.
        i = {}
        i['url'] = response.url
        return i

