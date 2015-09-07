from main.models import Proxy
import re, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "extract_data.settings")

from scrapy import Request, Spider
from scrap.items import MsaItem
from scrapy.utils.response import open_in_browser
import logging


class MsaSpider(Spider):
    name = "msa"
    allowed_domains = ["craigslist.org", "ipinfo.io"]
    start_urls = [
        # 'http://sandiego.craigslist.org',
        # 'http://atlanta.craigslist.org',
        'http://newyork.craigslist.org',
    ]
    use_proxy = True

    def parse(self, response):
        list_of_cities = response.xpath('//h5[text()="us cities"]/parent::li/ul//a[@href][text()!="more ..."]/@href').extract()
        # print list_of_cities
        for l in list_of_cities:
            r = Request(l + 'search/msa', callback=self.parse_city)
            r.meta['base_url'] = l[:-1]
            yield r

    def parse_city(self, response):
        links = response.xpath('//a[@class="hdrlnk"]/@href').extract()
        # logging.warning('N1 out !!!!')
        if not links:
            # logging.warning('N2 in !!!')
            yield Request(url=response.url, dont_filter=True)
        base_url = response.meta['base_url']
        for link in links:
            absolute_url = base_url + link
            if not Proxy.objects.filter(address=absolute_url).exists():
                yield Request(absolute_url, meta={'base_url': base_url},
                              callback=self.parse_attr)

        next_page = response.css("a.button.next::attr(href)")
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield Request(url, self.parse)

    def parse_attr(self, response):
        match = re.search(r"(\w+)\.html", response.url)
        if not match:
            return

        item_id = match.group(1)
        url = response.meta['base_url'] + "/reply/chi/vgm/" + item_id

        item = MsaItem()
        item["link"] = response.url
        item["title"] = "".join(response.xpath("//span[@class='postingtitletext']//text()").extract())
        item['body'] = "".join(response.xpath("//section[@id='ostingbody']/text()").extract())

        return Request(
            url, meta={'item': item}, callback=self.parse_contact,
            headers={"X-Requested-With": "XMLHttpRequest"})

    def parse_contact(self, response):
        item = response.meta['item']
        item["phone"] = ''
        item["email"] = "".join(response.xpath("//div[@class='anonemail']//text()").extract())
        tel = "".join(response.xpath("//b[text()='call']/following-sibling::ul[1]/li[1]/text()").extract())
        if tel:
            item["phone"] = tel.split(' ')[1]
        return item
