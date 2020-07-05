# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider

class CrawlItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()

class CrawlerxSpider(CrawlSpider):
    name = 'crawlerx'

    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]

        super(CrawlerxSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        for sel in response.xpath('//a'):
            item = CrawlItem()
            item['name'] = sel.xpath('text()').extract()
            item['link'] = sel.xpath('@href').extract()

            yield item

