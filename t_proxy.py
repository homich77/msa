import requests
import random
from threading import Thread
from Queue import Queue
import sys

# def checkproxy(proxy, timeout = 5, url="http://example.com", title="<title>Example Domain</title>"):
# def checkproxy(proxy, timeout = 10, url="http://sandiego.craigslist.org/", title="craigslist"):
def checkproxy(proxy, timeout = 10, url="http://washingtondc.craigslist.org/", title="craigslist"):
# def checkproxy(proxy, timeout = 10, url="http://google.com/", title="Google"):
    """
    Return True if proxy is alive, False if not
    Usage :
    checkproxy(proxy)
    checkproxy(proxy,10,'http://google.com','<title>Google</title>')
    """
    proxies = {
            "http" : "http://" + proxy,
            # "https" : "https://" +proxy
            }
    print url
    try :
        r = requests.get(url,proxies=proxies, timeout=timeout)
    except :
        return False
    return title in r.text and r.status_code in [200]


concurrent = 100

number_lines = 0
number_valid = 0
f = open('pl_usa_checked.txt','w')

def printProxy(status, proxy):
    global number_valid
    if status:
        proxy = 'http://'+proxy
        print proxy
        f.write(proxy+'\n')
        number_valid +=1

def CheckProxyList():
    while True:
        proxy = q.get()
        urls = ['http://atlanta.craigslist.org/', 'http://austin.craigslist.org/', 'http://boston.craigslist.org/', 'http://chicago.craigslist.org/', 'http://dallas.craigslist.org/', 'http://denver.craigslist.org/', 'http://detroit.craigslist.org/', 'http://houston.craigslist.org/', 'http://lasvegas.craigslist.org/', 'http://losangeles.craigslist.org/', 'http://miami.craigslist.org/', 'http://minneapolis.craigslist.org/', 'http://newyork.craigslist.org/', 'http://orangecounty.craigslist.org/', 'http://philadelphia.craigslist.org/', 'http://phoenix.craigslist.org/', 'http://portland.craigslist.org/', 'http://raleigh.craigslist.org/', 'http://sacramento.craigslist.org/', 'http://sandiego.craigslist.org/', 'http://seattle.craigslist.org/', 'http://sfbay.craigslist.org/', 'http://washingtondc.craigslist.org/']
        url = random.choice(urls)
        status = checkproxy(proxy, url = url)
        printProxy(status, proxy)
        q.task_done()


q = Queue(concurrent * 2)

for i in range(concurrent):
    t = Thread(target=CheckProxyList)
    t.daemon = True
    t.start()
try:
    # for proxy in open('proxy_list_orig.txt'):
    for proxy in open('pl_usa.txt'):
        number_lines += 1
        print 'proxy',proxy
        q.put(proxy.strip())
    q.join()

    print "[+] Checked {}".format(number_lines)
    print "[+] Valid {}".format(number_valid)
except KeyboardInterrupt:
    print
    print "Exiting"
    sys.exit(1)
f.close()