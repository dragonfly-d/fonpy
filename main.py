__author__ = 'Dimka'

from bs4 import BeautifulSoup
import os
import urllib2

img_size = "2000x1333"

web_page = urllib2.urlopen("http://www.goodfon.ru/").read()
soup = BeautifulSoup(web_page)


if not os.path.exists("D:\\pyfon\\"):
    os.makedirs("D:\\pyfon\\")

categories = {}
for i, a in enumerate(soup.find_all('a', {"class": "menu"})):
    if "/catalog/" in a.get('href'):
        categories[str(i)] = a.get('href').split("/")[2]
        print "%s %s" % (str(i), a.contents[0])

while True:
    category_num = raw_input("please input category number: ")
    if category_num in categories.keys():
        category = categories[category_num]
        print category
        break
    else:
        print "please specify correct category"

web_page = urllib2.urlopen("http://www.goodfon.ru/catalog/%s/" % category).read()
soup = BeautifulSoup(web_page)
for img in soup.find_all('img'):
    if "/wallpaper/" in img.get('src'):
        img_num = img.get('src').split("/")[5].replace("-n.jpg", "")
        url = img.get('src').replace("/wallpaper/previews", "/image").replace('-n', "-" + img_size)
        print url

        try:
            proxy = urllib2.ProxyHandler({'http': '119.46.110.17'})
            opener = urllib2.build_opener(proxy)
            urllib2.install_opener(opener)
            r = urllib2.urlopen(url)
            f = open("D:\\pyfon\\"+img_num+".jpg", 'wb')
            f.write(r.read())
            f.close()
            print "%s successfully loaded." % img_num

        except urllib2.HTTPError, e:
            if e.code == 404:
                print 'Cannot load image %s, no such size - %s.' % (img_num, e.code)
                continue
            if e.code == 503:
                print 'should use proxy -%s' % e.code
                continue