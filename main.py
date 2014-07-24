__author__ = 'Dim'

from bs4 import BeautifulSoup
import os
import urllib2

img_size = "1600x1200"
web_page = urllib2.urlopen("http://www.goodfon.ru/").read()
soup = BeautifulSoup(web_page)

img_path = raw_input("please specify folder to save (or live blank for default D:\pyfon): ")

if not img_path:
    img_path = "D:\\pyfon\\"

if not os.path.exists(img_path):
    os.makedirs(img_path)

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
            r = urllib2.urlopen(url)
            f = open(img_path + img_num + ".jpg", 'wb')
            f.write(r.read())
            f.close()
            print "%s successfully loaded." % img_num

        except urllib2.HTTPError, e:
            if e.code == 404:
                print 'Cannot load image %s, no such size or file - %s.' % (img_num, e.code)
                continue
            if e.code == 503:
                print 'should use proxy -%s' % e.code
                proxy_ip = "119.46.110.17"
                proxy = urllib2.ProxyHandler({'http': proxy_ip})
                opener = urllib2.build_opener(proxy)
                urllib2.install_opener(opener)
                print 'proxy -%s added' % proxy_ip
                continue
