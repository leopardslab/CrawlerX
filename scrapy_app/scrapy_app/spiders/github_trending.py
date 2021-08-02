from scrapy.spiders import CrawlSpider
from scrapy_app.spider_common import *


class GithubTrendingSpider(CrawlSpider):
    name = "github_trending"

    list_css_rules = {
        '.repo-list-item': {
            'repo_name': '.repo-list-name a::attr(href)',
            'repo_meta': '.repo-list-meta::text',
        }
    }

    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]
        self.settings = kwargs.get('settings')

        super(GithubTrendingSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        parsed_item = common_parser(self.settings)
        crawled_data = parse_with_rules(response, self.list_css_rules, dict)
        parsed_item['data'] = crawled_data
        yield parsed_item
