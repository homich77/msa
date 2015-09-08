# -*- coding: utf-8 -*-
import scrapy
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "extract_data.settings")
from scrap.items import PtfItem


class ProxylistUsaSpider(scrapy.Spider):
    name = "pl_usa"
    allowed_domains = ["us-proxy.org"]
    start_urls = (
        'http://www.us-proxy.org/',
    )
    use_proxy = False

    def parse(self, response):
        for tr in response.xpath('//tr'):
            http = 'http'
            if ''.join(tr.xpath('td[7]/text()').extract()) == 'yes':
                continue
                # http = 'https'
            ip = ''.join(tr.xpath('td[1]/text()').extract())
            port = ''.join(tr.xpath('td[2]/text()').extract())
            if ip and port:
                o = PtfItem()
                o['address'] = '%s:%s' % (ip, port)
                yield o
