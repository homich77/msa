# -*- coding: utf-8 -*-
import scrapy
import os
import re
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "extract_data.settings")
from scrap.items import PtfItem

class PrimeSpeedSpider(scrapy.Spider):
    name = "prime-speed"
    allowed_domains = ["www.prime-speed.ru"]
    start_urls = (
        'http://www.prime-speed.ru/proxy/free-proxy-list/all-working-proxies.php',
    )
    use_proxy = False

    def parse(self, response):
        ips = response.xpath("//pre/text()").extract()
        ip_list = ips[0].split('\n')
        expression = re.compile('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{2,4}$')
        for ip_port in ip_list:
            if expression.match(ip_port) and not ip_port == '0.0.0.0:80':
                o = PtfItem()
                o['address'] = ip_port
                yield o