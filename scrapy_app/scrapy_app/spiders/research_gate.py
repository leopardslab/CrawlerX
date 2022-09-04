import scrapy
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from scrapy_app.spider_common import common_parser

from scrapy import Request
from requests_html import HTML

import json
import os


BASE_URL = "https://www.researchgate.net/"

# request token
RG_REQUEST_TOKEN = "//meta[@name='Rg-Request-Token']"

# paper info
TITLE = "//h1/text()"
DATE = "//div[@class='research-detail-header-section__metadata']/div[1]//li/text()"
DOI = "//div[contains(text(),'DOI:')]/a/text()"
CONFERENCE = "//li[contains(text(),'Conference:')]/text()"
CITATIONS_COUNT = "//div[contains(text(),'Citations')]/text()"
REFERENCES_COUNT = "//div[contains(text(),'References')]/text()"


# references section
REFERENCES = "//div[@class='js-target-reference']//div[@class='nova-v-citation-item']"
# references title
REFERENCES_TITLE = ".//div[contains(@class,'nova-v-publication-item__title')]/a/text()"
# referecnes hyper link (might be null)
REFERENCES_LINK = ".//div[contains(@class,'nova-v-publication-item__title')]//@href"
# references type (eg. Article, Conference Paper, Null)
REFERENCES_TYPE = ".//span[contains(@class,'nova-v-publication-item__type')]/text()"
# references authors
REFERENCES_AUTHOR = ".//ul[contains(@class,'nova-v-publication-item__person-list')]/text()"
# references date
REFERENCES_DATE = ".//div[@class='nova-v-publication-item__meta-right']//span/text()"


def transform_number(s):
    s = s[s.find("(")+1:s.find(")")]
    return int(s.replace(",",""))
    

class ResearchGateSpider(CrawlSpider):
    name = "research_gate"

    custom_settings = {
        'LOG_LEVEL': 'INFO',
        'DEPTH_LIMIT': 1,
        'DOWNLOAD_DELAY': 5,
    }


    def start_requests(self):
        yield scrapy.Request(self.url)


    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]
        self.settings = kwargs.get('settings')

        super(ResearchGateSpider, self).__init__(*args, **kwargs)


    def parse(self, response):
        parsed_item = common_parser(self.settings)
        follow_urls = set()

        paper_info = {
           'title': response.xpath(TITLE).get(),
           'url': response.url,
           'date': response.xpath(DATE).get(),
           'DOI': response.xpath(DOI).get(),
           'conference': response.xpath(CONFERENCE).get(),
           'citation count': transform_number(response.xpath(CITATIONS_COUNT).get()),
           'reference count': transform_number(response.xpath(REFERENCES_COUNT).get())
        }

        publication_id = paper_info['url'][paper_info['url'].find("publication")+12:paper_info['url'].find("_")]
        request_token = response.xpath(RG_REQUEST_TOKEN).attrib['content']
        offset = 10

        if get_reference(token=request_token, uid=publication_id, offset=offset).status_code != 200:
            self.logger.info(f"response status {get_reference(uid=publication_id, offset=offset).status_code} instead of 200, possibly need to update cookies & token")

        while get_reference(token=request_token, uid=publication_id, offset=offset).status_code == 200:
            ref_response = get_reference(token=request_token, uid=publication_id, offset=offset)
            if (ref_response.text == ''):
                break
            html = HTML(html=ref_response.text)
            links = html.xpath(REFERENCES_LINK)
            if len(links) == 0:
                break
            for link in links:
                follow_urls.add(BASE_URL+link)
            offset = offset + 5

        for reference in response.xpath(REFERENCES):
            reference_link = BASE_URL+reference.xpath(REFERENCES_LINK).get() if reference.xpath(REFERENCES_LINK).get() is not None else ""
            if (reference_link != ''):
                follow_urls.add(reference_link)

        self.logger.info(f"total urls to follow: {len(follow_urls)}")

        references = []
        for url in follow_urls:
            if url is not None:
                references.append(response.follow(url, self.reference_parse))
        
        paper_info['references'] = references
        parsed_item['data'] = paper_info
        yield parsed_item


    def reference_parse(self, response):
        ref_info = {
            'reference title': response.xpath(TITLE).get(),
            'url': response.url,
            'date': response.xpath(DATE).get(),
            'DOI': response.xpath(DOI).get(),
            'conference': response.xpath(CONFERENCE).get(),
            'citation count': transform_number(response.xpath(CITATIONS_COUNT).get()),
        }

        return ref_info
