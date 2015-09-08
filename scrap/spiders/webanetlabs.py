# -*- coding: utf-8 -*-
import scrapy
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "extract_data.settings")
from scrap.items import PtfItem
from scrapy import Request


class WALSpider(scrapy.Spider):
    name = "wal"
    allowed_domains = ["webanetlabs.net"]
    start_urls = (
        'http://webanetlabs.net/publ/24',
    )
    use_proxy = False

    def parse(self, response):
        url = 'http://webanetlabs.net' + response.xpath('//div[@class="uSpoilerText"]/a/@href').extract()[0]
        yield Request(url, callback=self.parse_txt)

    def parse_txt(self, response):
        data = filter(lambda x: ord(x) < 128, response.body)
        data = data.split('\r\n')
        for ip_port in data:
            if not ip_port:
                continue
            o = PtfItem()
            o['address'] = ip_port
            yield o
