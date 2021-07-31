import os
from scrapy.spiders import CrawlSpider
from scrapy.item import Item, Field
from scrapy_app.spider_common import *


class RedditItem(Item):
    name = Field()


class RedditSpider(CrawlSpider):
    name = "reddit"
    auto_join_text = False
    keywords = {'__use', '__list'}
    list_css_rules = {
        '.link': {
            'title': '.title a::text',
            'domain': '.domain a::text',
            'author': '.author::text',
            'comment_count': '.comments::text',
            'score': '.score::text',
        }
    }
    content_css_rules = {
        'text': '#Cnt-Main-Article-QQ p *::text',
        'images': '#Cnt-Main-Article-QQ img::attr(src)',
        'images-desc': '#Cnt-Main-Article-QQ div p+ p::text',
    }

    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]
        self.settings = kwargs.get('settings')

        super(RedditSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        parsed_item = dict()
        parsed_settings = dict(self.settings)
        parsed_item['user_id'] = parsed_settings['user_id']
        parsed_item['project_name'] = parsed_settings['project_name']
        parsed_item['job_name'] = parsed_settings['job_name']
        parsed_item['unique_id'] = parsed_settings['unique_id']
        parsed_item['schedule_time'] = parsed_settings['schedule_time']
        parsed_item['task_id'] = os.environ['SCRAPY_JOB']
        crawled_data = parse_with_rules(response, self.list_css_rules, dict)
        parsed_item['data'] = crawled_data
        yield parsed_item
