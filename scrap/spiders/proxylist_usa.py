# -*- coding: utf-8 -*-
import scrapy
# from scrap.items import PtfItem

# settings.overrides['HTTP_PROXY'] = 300 
use_proxy = 'False'

class ProxylistUsaSpider(scrapy.Spider):
    name = "pl_usa"
    allowed_domains = ["us-proxy.org"]
    start_urls = (
        'http://www.us-proxy.org/',
    )

    def parse(self, response):
        print response.url
        # item = PtfItem()
        # item['ip'] = "".join(response.xpath('//tr/td[1]/text()').extract())
        # item['port'] = "".join(response.xpath('//tr/td[2]/text()').extract())
        ips_list = response.xpath('//tr/td[1]/text()').extract()
        ports_list = response.xpath('//tr/td[2]/text()').extract()
        with open('pl_usa.txt', 'w') as f:
            for ip in ips_list:
                f.writelines(ip+":"+ports_list.pop(0)+'\n')
        # for
        # return item
        # pass
