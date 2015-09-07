import os
import random
import urllib2

from user_agents import USER_AGENTS
from scrapy.conf import settings


class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        ua = random.choice(USER_AGENTS)
        if ua:
            request.headers.setdefault('User-Agent', ua)


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        # request.meta['proxy'] = "http://104.171.126.86:7808"
        pass
        # response = urllib2.urlopen('https://api.ipify.org?format=json')
        # print response.read()
        # request.meta['proxy'] = settings.get('HTTP_PROXY')
