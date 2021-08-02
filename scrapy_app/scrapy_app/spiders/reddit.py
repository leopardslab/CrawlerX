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
        parsed_item = common_parser(self.settings)
        crawled_data = parse_with_rules(response, self.list_css_rules, dict)
        parsed_item['data'] = crawled_data
        yield parsed_item
