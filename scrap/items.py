# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MsaItem(scrapy.Item):
    link = scrapy.Field()
    title = scrapy.Field()
    email = scrapy.Field()
    phone = scrapy.Field()
    body = scrapy.Field()


class PtfItem(scrapy.Item):
    address = scrapy.Field()
