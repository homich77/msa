# -*- coding: utf-8 -*-
import scrapy
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "extract_data.settings")
from scrap.items import PtfItem
from scrapy.utils.response import open_in_browser


class GatherProxySpider(scrapy.Spider):
    name = "gp"
    allowed_domains = ["gatherproxy.com"]
    start_urls = (
        'http://www.gatherproxy.com/',
    )
    use_proxy = False

    def parse(self, response):
        # open_in_browser(response)
        print response.xpath('//table[@id="tblproxy"]/tr').extract()
        for tr in response.xpath('//table[@id="tblproxy"]//tr[@port]'):
            print ''.join(tr.xpath('@prx').extract()), ''.join(tr.xpath('@tmres').extract())
