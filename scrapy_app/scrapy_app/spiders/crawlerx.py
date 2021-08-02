import scrapy
from scrapy.spiders import CrawlSpider
from scrapy_app.spider_common import common_parser


class CrawlItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()


# default spider for retrieve href in the given URL
class CrawlerxSpider(CrawlSpider):
    name = 'crawlerx'

    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]
        self.settings = kwargs.get('settings')

        super(CrawlerxSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        parsed_item = common_parser(self.settings)
        crawled_data = []
        for sel in response.xpath('//a'):
            item = CrawlItem()
            item['name'] = sel.xpath('text()').extract()
            item['link'] = sel.xpath('@href').extract()
            crawled_data.append(item)

        parsed_item['data'] = crawled_data
        yield parsed_item
