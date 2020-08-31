import os
import scrapy
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider


class CrawlItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()


class StackOverflowSpider(CrawlSpider):
    name = "stackoverflow"

    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]
        self.settings = kwargs.get('settings')

        super(StackOverflowSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        parsed_item = dict()
        parsed_settings = dict(self.settings)
        parsed_item['user_id'] = parsed_settings['user_id']
        parsed_item['project_name'] = parsed_settings['project_name']
        parsed_item['job_name'] = parsed_settings['job_name']
        parsed_item['unique_id'] = parsed_settings['unique_id']
        parsed_item['task_id'] = os.environ['SCRAPY_JOB']

        crawled_data = []
        questions = Selector(response).xpath('//div[@class="summary"]/h3')
        for question in questions:
            item = CrawlItem()
            item['title'] = question.xpath(
                'a[@class="question-hyperlink"]/text()').extract()[0]
            item['link'] = question.xpath(
                'a[@class="question-hyperlink"]/@href').extract()[0]
            crawled_data.append(item)

        parsed_item['data'] = crawled_data
        yield parsed_item