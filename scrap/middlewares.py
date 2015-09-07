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
        self.proxies = Proxy.objects.filter(status__gt=0)\
            .values_list('address', flat=True)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        # Don't overwrite with a random one (server-side state for IP)
        if not spider.use_proxy:
            return
        # if 'proxy' in request.meta:
        #     return
        if not len(self.proxies):
            return

        proxy = random.choice(self.proxies)
        request.meta['proxy'] = proxy
        logging.debug("ASSIGNED PROXY %s" % proxy)
        # if proxy_user_pass:
        #     basic_auth = 'Basic ' + base64.encodestring(proxy_user_pass)
        #     request.headers['Proxy-Authorization'] = basic_auth

    def process_exception(self, request, exception, spider):
        if not spider.use_proxy:
            return
        proxy_address = request.meta['proxy']
        # print 'EXCEPTION: %s' % proxy
        logging.warning('Removing failed proxy <%s>, %d proxies left' %
                        (proxy_address, len(self.proxies)))
        try:
            self.proxies.remove(proxy_address)
            p = Proxy.objects.get(address=proxy_address, status__gt=0)
            if p:
                p.status = -1
                p.save()
        except ValueError:
            pass
