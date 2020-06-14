from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class WikipediaSpider(CrawlSpider):
    name = "wikipedia"

    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]

        WikipediaSpider.rules = [
            Rule(LinkExtractor(unique=True), callback='parse_item'),
        ]
        super(WikipediaSpider, self).__init__(*args, **kwargs)

    def parse_item(self, response):
        # first extract title of page
        title = response.css('title::text').get()
        yield {
            'title': title
        }
        # now follow links to other pages
        for href in response.css('li a::attr(href)').getall():
            yield response.follow(href, callback=self.parse_item)