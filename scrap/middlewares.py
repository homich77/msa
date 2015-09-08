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
            p = Proxy.objects.filter(address=proxy_address)
            if p:
                p = p[0]
                p.status = -1
                p.save()
        except ValueError:
            pass

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
        request.meta['proxy'] = proxy
        logging.debug("ASSIGNED PROXY %s" % proxy)

    def process_exception(self, request, exception, spider):
        if not spider.use_proxy:
            return
        proxy_address = request.meta['proxy']
        # print 'EXCEPTION: %s' % proxy
        logging.warning('Removing failed proxy <%s>, %d proxies left' %
                        (proxy_address, len(self.proxies)))
        self.save_failed_proxy(proxy_address)
