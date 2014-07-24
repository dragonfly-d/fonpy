__author__ = 'Dmitiy'

from bs4 import BeautifulSoup
import urllib2
proxies = []


def getProxyList():
    pages_to_scan = 1
    i = 1
    while i <= pages_to_scan:
        web_page = urllib2.urlopen("http://proxy-list.org/russian/index.php?p=%s" % str(i)).read()
        soup = BeautifulSoup(web_page)
        td = soup.find_all("li", {"class": "proxy"})

        for ip in td[1:]:
            proxies.append(ip.contents[0])
        i += 1

    return proxies




