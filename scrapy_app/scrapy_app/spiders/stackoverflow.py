# from scrapy import Spider
# from scrapy.selector import Selector
#
# from scrapy_app.scrapy_app.items import ScrapyAppItem
#
#
# class CrawlerxSpider(Spider):
#     name = "stackoverflow"
#     allowed_domains = ["stackoverflow.com"]
#     start_urls = [
#         "http://stackoverflow.com/questions?pagesize=50&sort=newest",
#     ]
#
#     def parse(self, response):
#         questions = Selector(response).xpath('//div[@class="summary"]/h3')
#
#         for question in questions:
#             item = ScrapyAppItem()
#             item['title'] = question.xpath(
#                 'a[@class="question-hyperlink"]/text()').extract()[0]
#             item['url'] = question.xpath(
#                 'a[@class="question-hyperlink"]/@href').extract()[0]
#             yield item