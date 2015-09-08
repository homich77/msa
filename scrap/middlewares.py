import os
import random
import urllib2
import logging

from main.models import Proxy
from user_agents import USER_AGENTS
# from scrapy.conf import settings


class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        ua = random.choice(USER_AGENTS)
        if ua:
            request.headers.setdefault('User-Agent', ua)


class RandomProxy(object):
    def __init__(self, settings):
        # self.proxies = ['http://46.149.86.215:8080',
        #                 'http://218.207.212.79:80']
        self.proxies = list(Proxy.objects.filter(status__gt=0)\
                            .values_list('address', flat=True)[:4])
        print 'PROXIES %s' % self.proxies

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def save_failed_proxy(self, proxy_address):
        try:
            self.proxies.remove(proxy_address)
            p = self.get_proxy_model(proxy_address)
            if p:
                p.status = -1
                p.save()
        except ValueError:
            pass

    def get_proxy_model(self, address):
        p = Proxy.objects.filter(address=address)
        if not p:
            return False
        return p[0]

    def process_request(self, request, spider):
        # Don't overwrite with a random one (server-side state for IP)
        retry_times = request.meta.get('retry_times', 0)
        if 'reply' not in request.url\
                or 'proxy' in request.meta and retry_times < 3 \
                or not spider.use_proxy \
                or not len(self.proxies):
            return

        print 'url: %s. retry: %s' % (request.url, retry_times)
        if retry_times > 0:
            self.save_failed_proxy(request.meta['proxy'])

        proxy = random.choice(self.proxies)
        if 'http' not in proxy:
            p = self.get_proxy_model(proxy)
            proxy = 'http://' + proxy
            if p:
                if not Proxy.objects.filter(address=proxy).exists():
                    p.address = proxy
                    p.save()

        request.meta['proxy'] = proxy
        logging.debug("ASSIGNED PROXY %s" % proxy)

    def process_exception(self, request, exception, spider):
        if not spider.use_proxy:
            return
        proxy_address = request.meta.get('proxy', '')
        # print 'EXCEPTION: %s' % proxy

        if proxy_address:
            logging.warning('Removing failed proxy <%s>, %d proxies left' %
                            (proxy_address, len(self.proxies)))
            self.save_failed_proxy(proxy_address)
