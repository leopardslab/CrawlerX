import os
import re
import unicodedata
from scrapy.spiders import CrawlSpider


class WikipediaSpider(CrawlSpider):
    name = "wikipedia"

    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]
        self.settings = kwargs.get('settings')

        super(WikipediaSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        parsed_item = dict()
        parsed_settings = dict(self.settings)
        parsed_item['user_id'] = parsed_settings['user_id']
        parsed_item['project_name'] = parsed_settings['project_name']
        parsed_item['job_name'] = parsed_settings['job_name']
        parsed_item['unique_id'] = parsed_settings['unique_id']
        parsed_item['schedule_time'] = parsed_settings['schedule_time']
        parsed_item['task_id'] = os.environ['SCRAPY_JOB']

        crawled_data = []
        def _clean(value):
            value = ' '.join(value)
            value = value.replace('\n', '')
            value = unicodedata.normalize("NFKD", value)
            value = re.sub(r' , ', ', ', value)
            value = re.sub(r' \( ', ' (', value)
            value = re.sub(r' \) ', ') ', value)
            value = re.sub(r' \)', ') ', value)
            value = re.sub(r'\[\d.*\]', ' ', value)
            value = re.sub(r' +', ' ', value)
            return value.strip()

        strings = []
        for i in range(0, 100):
            try:
                for node in response.xpath('//*[@id="mw-content-text"]/div/p[{}]'.format(i)):
                    text = _clean(node.xpath('string()').extract())
                    if len(text):
                        strings.append(text)
            except Exception as error:
                strings.append(str(error))
        info_card = dict()
        i = 0
        rows = response.xpath('//*[@id="mw-content-text"]/div/table[@class="infobox vcard" ]/tr')
        for row in rows:
            # Scraping Image in info box
            value = dict()
            if row.css('.image'):
                if row.css('img'):
                    i += 1
                    item = 'Logo_{}'.format(i)
                    try:
                        value['logo_thumb_url'] = row.css('img').xpath('@src').extract_first().replace('//', '')
                        try:
                            value['logo_url'] = self.domain + row.css('a::attr(href)').extract_first()[1:]
                            try:
                                text = _clean(row.xpath('string()').extract())
                                if text:
                                    value['text'] = text
                            except:
                                pass
                        except:
                            pass
                    except:
                        pass

            # Scraping info box values
            elif row.xpath('th'):
                item = row.xpath('th//text()').extract()
                item = [_.strip() for _ in item if _.strip() and _.replace('\n', '')]
                item = ' '.join(item)
                item = item.replace('\n', '')
                item = unicodedata.normalize("NFKD", item)
                item = re.sub(r' +', ' ', item)
                item = item.strip()

                if row.xpath('td/div/ul/li'):
                    value = []
                    for li in row.xpath('td/div/ul/li'):
                        value.append(''.join(li.xpath('.//text()').extract()))
                    value = [_.strip() for _ in value if _.strip() and _.replace('\n', '')]
                    value = ', '.join(value)
                else:
                    value = row.xpath('td//text()').extract()
                    value = [_.strip() for _ in value if _.strip() and _.replace('\n', '')]

                    if item == 'Website':
                        value = ''.join(value)
                    else:
                        value = ' '.join(value)

                value = value.replace('\n', '')
                value = unicodedata.normalize("NFKD", value)
                value = re.sub(r' , ', ', ', value)
                value = re.sub(r' \( ', ' (', value)
                value = re.sub(r' \) ', ') ', value)
                value = re.sub(r' \)', ') ', value)
                value = re.sub(r'\[\d\]', ' ', value)
                value = re.sub(r' +', ' ', value)
                value = value.strip()
                info_card[item] = value
        crawled_data.append({
            'Title': response.css('#firstHeading::text').extract_first(),
            'Organization_name': response.css('#mw-content-text > div >'
                                              ' table.infobox.vcard > caption::text').extract_first(),
            **info_card,
            'strings': strings
        })

        parsed_item['data'] = crawled_data
        yield parsed_item
