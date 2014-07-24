__author__ = 'Dmitiy'

from bs4 import BeautifulSoup
import urllib2
web_page = urllib2.urlopen("http://www.freeproxylists.net/ru/").read()
soup = BeautifulSoup(web_page)