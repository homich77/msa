import requests
import sys
import urllib2
import json

from scrap.spiders.msa import MsaSpider
from scrap.spiders.webanetlabs import WALSpider
from scrap.spiders.prime_speed import PrimeSpeedSpider
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "extract_data.settings")

from main.models import Proxy
from threading import Thread
from Queue import Queue
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrap.spiders.proxylist_usa import ProxylistUsaSpider

class GetProxies(object):
    def __init__(self, start_main_spider=False):
        self.urls = [
            {
                'url': 'https://happy-proxy.com/fresh_proxies?key=6fd3e79b99a7be9b',
                'ip': 'ip_port',
                'port_in_ip': True
            }, {
                'url': 'http://proxy.tekbreak.com/200/json',
                'port_in_ip': False
            }]
        self.spiders = [ProxylistUsaSpider, WALSpider, PrimeSpeedSpider]
        self.proxies = []
        self.get()

        ch = CheckProxy()
        ch.set_proxies_list()

        if start_main_spider:
            process = CrawlerProcess(get_project_settings())
            process.crawl(MsaSpider)
            process.start()

    def get(self):
        for proxy in self.urls:
            print '*'*50
            print 'Open url: %s' % proxy['url']
            response = urllib2.urlopen('http://'+proxy['url'])

            data = json.loads(response.read())
            print 'Get %s proxies' % len(data)
            for d in data:
                self.save(self.get_ip_port(d, proxy))

        # Get proxies from spiders
        process = CrawlerProcess(get_project_settings())
        for s in self.spiders:
            process.crawl(s)
        process.start()

    def save(self, data):
        try:
            p, created = Proxy.objects.get_or_create(**data)
            # Proxy.objects.bulk_create(self.proxies)
            if created:
                print 'Saved into DB : %s' % data
        except Exception, e:
            print 'Error in saving into DB: %s' % str(e)

    def get_ip_port(self, data, proxy):
        address = data[proxy.get('ip', 'ip')]
        if not proxy['port_in_ip']:
            address += ':' + data[proxy.get('port', 'port')]
        return {'address': address}


class CheckProxy(object):
    def __init__(self):
        self.concurrent = 10
        self.number_lines = 0
        self.success_proxies = 0
        self.failed_proxies = 0
        self.timeout = 60
        self.q = Queue()
        self.prepare_threads()
        print '\nPreparing to check proxies...\n'

    def prepare_threads(self):
        for i in range(self.concurrent):
            t = Thread(target=self.get_queue_item)
            t.daemon = True
            t.start()

    def set_proxies_list(self):
        try:
            for proxy in Proxy.objects.filter(status=0):
                self.q.put(proxy.address)

            self.q.join()
            self.print_result()
        except KeyboardInterrupt:
            print "\nExiting"
            sys.exit(1)

    def get_queue_item(self):
        while True:
            try:
                proxy = self.q.get()
                self.number_lines += 1
            except Exception, e:
                print 'ERROR: %s' % str(e)
                continue

            self.check_proxy(proxy)
            self.q.task_done()

    def check_proxy(self, proxy, url="http://sandiego.craigslist.org/"):
        """
        Return True if proxy is alive, False if not
        Usage :
        checkproxy(proxy)
        checkproxy(proxy,10,'http://google.com')
        """
        p = Proxy.objects.get(address=proxy)
        try:
            # print proxy
            r = requests.get(url, proxies={
                "http": proxy,
            }, timeout=self.timeout)

            p.last_status_code = r.status_code

            if r.status_code > 400:
                self.save_failed_proxy(p, r.status_code)
            else:
                p.status = r.elapsed.total_seconds()
                if p.status == 0:
                    p.status = 1
                self.success_proxies += 1
                print '%s. %s: %s' % (self.success_proxies, proxy, r.status_code)
                p.save()

        except Exception, e:
            self.save_failed_proxy(p, 0)
            return False

    def save_failed_proxy(self, proxy_model, error):
        proxy_model.status = -1
        proxy_model.save()
        self.failed_proxies += 1
        print '%s. %s: %s' % (self.failed_proxies, proxy_model.address, error)

    def print_result(self):
        print "[+] Checked %s" % self.number_lines
        print "[+] Valid %s" % self.success_proxies
        print "[+] InValid %s" % self.failed_proxies


if __name__ == '__main__':
    g = GetProxies(sys.argv[1])
