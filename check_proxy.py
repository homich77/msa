import requests

from threading import Thread
from Queue import Queue
import sys


class CheckProxy(object):
    def __init__(self):
        self.concurrent = 200
        self.number_lines = 0
        self.timeout = 60
        self.q = Queue()
        self.success_proxies = []
        self.failed_proxies = []

        self.prepare_threads()

    def prepare_threads(self):
        for i in range(self.concurrent):
            t = Thread(target=self.get_queue_item)
            t.daemon = True
            t.start()

    def set_proxies_list(self, file_name='proxy_list.py'):
        try:
            for proxy in open(file_name):
                if not proxy:
                    continue
                self.number_lines += 1
                # if self.number_lines > 10:
                #     break
                self.q.put(proxy.strip())

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

    def check_proxy(self, proxy, url="http://sandiego.craigslist.org/",
                    title="craigslist"):
        """
        Return True if proxy is alive, False if not
        Usage :
        checkproxy(proxy)
        checkproxy(proxy,10,'http://google.com','<title>Google</title>')
        """
        try:
            r = requests.get(url, proxies={
                "http": "http://" + proxy,
            }, timeout=self.timeout)
            
            if r.status_code > 400:
                self.failed_proxies.append('%s %s ' % (proxy, r.status_code))
                if len(self.failed_proxies) % 10 == 0 or r.elapsed.total_seconds() > 20:
                    print 'Failed list has %s length. %s seconds' % \
                          (len(self.failed_proxies), r.elapsed.total_seconds())
            else:
                self.success_proxies.append(proxy)
                print '%s. %s: %s' % (len(self.success_proxies), proxy, r.status_code)
        except Exception, e:
            # print 'ERROR from checkproxy: %s' % str(e)
            return False

    def print_result(self):
        print "[+] Checked %s" % self.number_lines
        print "[+] Valid %s" % len(self.success_proxies)

        with open('pl_usa_checked.txt', 'w+') as success_file:
            success_file.writelines('\n'.join(self.success_proxies))
        with open('failed_proxy.txt', 'w+') as failed_file:
            failed_file.writelines('\n'.join(self.failed_proxies))


if __name__ == '__main__':
    ch = CheckProxy()
    ch.set_proxies_list(file_name='pl_usa.txt')
