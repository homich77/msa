import re

from scrapy import Request, Spider
from scrap.items import PtfItem
from scrapy.utils.response import open_in_browser
import logging

class PtfSpider(Spider):
    name = "ptf"
    allowed_domains = ["www.us-proxy.org"]
    start_urls = [
        'http://www.us-proxy.org'
        # 'http://atlanta.craigslist.org'
        # 'http://ipinfo.io/json'
    ]

    # def parse(self, response):
        # print response.body
# response.xpath('//tr/td[1]/text()').extract()
# response.xpath('//tr/td[2]/text()').extract()

    def parse(self, response):
        item = PtfItem()
        item['ip'] = "".join(response.xpath('//tr/td[1]/text()').extract())
        item['port'] = "".join(response.xpath('//tr/td[2]/text()').extract())

        # return
        # for l in list_of_cities:
        #     r = Request(l + 'search/msa', callback=self.parse_city)
        #     r.meta['base_url'] = l[:-1]
        #     yield r

    # def parse_city(self, response):
    #     links = response.xpath('//a[@class="hdrlnk"]/@href').extract()
    #     logging.warning('N1 out !!!!')
    #     if not links:
    #         logging.warning('N2 in !!!')
    #         yield Request(url=response.url, dont_filter=True)
    #     base_url = response.meta['base_url']
    #     for link in links:
    #         absolute_url = base_url + link
    #         yield Request(absolute_url, meta={'base_url': base_url},
    #                       callback=self.parse_attr)
    #         return
    #     return
    #
    #     next_page = response.css("a.button.next::attr(href)")
    #     if next_page:
    #         url = response.urljoin(next_page[0].extract())
    #         yield Request(url, self.parse)
    #
    # def parse_attr(self, response):
    #     match = re.search(r"(\w+)\.html", response.url)
    #     if not match:
    #         return
    #
    #     item_id = match.group(1)
    #     # url = response.meta['base_url'] + "/reply/chi/vgm/" + item_id
    #     url = "http://mf2gyyloorqq.mnzgc2lhonwgs43ufzxxezy.cmle.ru/reply/chi/vgm/" + item_id
    #
    #     item = MsaItem()
    #     item["link"] = response.url
    #     item["title"] = "".join(response.xpath("//span[@class='postingtitletext']//text()").extract())
    #     item['body'] = "".join(response.xpath("//section[@id='ostingbody']/text()").extract())
    #
    #     return Request(
    #         url, meta={'item': item}, callback=self.parse_contact,
    #         headers={"X-Requested-With": "XMLHttpRequest"})
    #
    # def parse_contact(self, response):
    #     item = response.meta['item']
    #     item["phone"] = ''
    #     item["email"] = "".join(response.xpath("//div[@class='anonemail']//text()").extract())
    #     tel = "".join(response.xpath("//b[text()='call']/following-sibling::ul[1]/li[1]/text()").extract())
    #     if tel:
    #         item["phone"] = tel.split(' ')[1]
    #     return item
