from main.models import Proxy
import requests

from threading import Thread
from Queue import Queue
import sys


class CheckProxy(object):
    def __init__(self):
        self.concurrent = 200
        self.number_lines = 0
        self.success_proxies = 0
        self.timeout = 60
        self.q = Queue()

        self.prepare_threads()

    def prepare_threads(self):
        for i in range(self.concurrent):
            t = Thread(target=self.get_queue_item)
            t.daemon = True
            t.start()

    def set_proxies_list(self):
        try:
            for proxy in Proxy.objects.filter(status=0):
                self.number_lines += 1
                # if self.number_lines > 10:
                #     break
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
        try:
            r = requests.get(url, proxies={
                "http": proxy,
            }, timeout=self.timeout)

            p = Proxy.objects.get(address=proxy)
            p.last_status_code = r.status_code
            if r.status_code > 400:
                p.status = -1
            else:
                p.status = r.elapsed.total_seconds()
                self.success_proxies += 1
                print '%s. %s: %s' % (self.success_proxies, proxy, r.status_code)
            p.save()
        except Exception, e:
            # print 'ERROR from checkproxy: %s' % str(e)
            return False

    def print_result(self):
        print "[+] Checked %s" % self.number_lines
        print "[+] Valid %s" % self.success_proxies


if __name__ == '__main__':
    ch = CheckProxy()
    ch.set_proxies_list()
