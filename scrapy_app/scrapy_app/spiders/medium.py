import scrapy
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from scrapy_app.spider_common import common_parser


class MediumSpider(CrawlSpider):
    name = "medium"
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_DEBUG': True,
        'DOWNLOAD_DELAY': 1,
        'ROBOTSTXT_OBEY': True,
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
    }

    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]
        self.settings = kwargs.get('settings')

        super(MediumSpider, self).__init__(*args, **kwargs)

    def parse_articles(self, response):
        parsed_item = common_parser(self.settings)
        articles = response.xpath('/html/body/div[1]/div[2]/div/div[3]/div[1]/div[2]/*')
        crawled_data = []
        if len(articles) != 0:
            for article in articles:
                author = article.xpath('.//a[@data-action="show-user-card"]/text()').get()

                str_read_time = article.xpath('.//*[@class="readingTime"]/@title')[0].get()
                int_read_time = str_read_time.split()[0]

                collection = article.xpath('.//a[@data-action="show-collection-card"]/text()').get()

                title = article.xpath('.//h3[contains(@class, "title")]/text()').get()

                claps = article.xpath('.//button[@data-action="show-recommends"]/text()').get()
                if claps != None:
                    claps = claps.split()[0]               
                    if type(claps) == str:
                        claps = text_to_num(claps)

                responses = article.xpath('.//a[@class="button button--chromeless u-baseColor--buttonNormal"]/text()').get()
                if responses != None:
                    responses = responses.split()[0]

                subtitle_preview = article.xpath('.//h4[@name="previewSubtitle"]/text()').get()

                published_date = article.xpath('.//time/text()').get()
                try:
                    date_object = datetime.strptime(published_date, "%b %d, %Y")
                    year = date_object.year
                except:
                    date_object = datetime.strptime(published_date, "%b %d")
                    year = datetime.now().year
                day = date_object.day
                month = date_object.month
                published_date = datetime(year, month, day)

                article_url = article.xpath('.//a[contains(@class, "button--smaller")]/@href').get().split('?')[0]
                scraped_date = datetime.now()

                item =  {
                    'author': author,
                    'title': title,
                    'subtitle preview': subtitle_preview,
                    'collection': collection,
                    'read time': int_read_time,
                    'claps': claps,
                    'responses': responses,
                    'published_date': published_date,
                    'article_url' : article_url,
                    'scraped_date': scraped_date
                }
                crawled_data.append(item)
        parsed_item['data'] = crawled_data
        yield parsed_item

def text_to_num(text):
    d = {'K': 3}
    if text[-1] in d:
        num, magnitude = text[:-1], text[-1]
        return int(Decimal(num) * 10 ** d[magnitude])
    else:
        return int(Decimal(text))
        