__author__ = 'dragonfly_d'

from bs4 import BeautifulSoup
import os
import urllib2
from proxy_collecter import getProxyList


img_size = "1600x1200"

categories = {}
web_page = urllib2.urlopen("http://www.goodfon.ru/").read()
soup = BeautifulSoup(web_page)

img_path = raw_input("please specify folder to save (or live blank for default D:\pyfon): ")

if img_path:
    if not img_path.endswith("\\"):
        img_path += "\\"
else:
    img_path = "D:\\pyfon\\"

if not os.path.exists(img_path):
    os.makedirs(img_path)

for i, a in enumerate(soup.find_all('a', {"class": "menu"})):
    if "/catalog/" in a.get('href'):
        categories[str(i)] = a.get('href').split("/")[2]
        print "%s %s" % (str(i), a.contents[0])

while True:
    category_num = raw_input("please input category number: ")
    if category_num in categories.keys():
        category = categories[category_num]
        break
    else:
        print "please specify correct category"

web_page = urllib2.urlopen("http://www.goodfon.ru/catalog/%s/" % category).read()
soup = BeautifulSoup(web_page)

px_counter = 0
for img in soup.find_all('img'):
    if "/wallpaper/" in img.get('src'):
        img_num = img.get('src').split("/")[5].replace("-n.jpg", "")
        url = img.get('src').replace("/wallpaper/previews", "/image").replace('-n', "-" + img_size)

        try:
            print "downloading image %s " % img_num
            r = urllib2.urlopen(url)
            f = open(img_path + img_num + ".jpg", 'wb')
            f.write(r.read())
            f.close()
            print "%s successfully loaded." % img_num

        except urllib2.HTTPError, e:
            if e.code == 404:
                print 'Cannot download image %s, no such size (or file) - %s.' % (img_num, e.code)
                continue

            if e.code == 503:
                print "Cannot download %s. Reason: download limit exceeded ($s)\ntrying to get proxies..." % (img_num, e.code)
                px = getProxyList()
                if len(px) > 0:
                    try:
                        print "proxies successfully recieved."
                        proxy_ip = px[px_counter]
                        print proxy_ip, " - proxy ip \ndownloading image %s" % img_num
                        proxy = urllib2.ProxyHandler({'http': proxy_ip})
                        opener = urllib2.build_opener(proxy)
                        urllib2.install_opener(opener)
                        r = urllib2.urlopen(url)
                        f = open(img_path + img_num + ".jpg", 'wb')
                        f.write(r.read())
                        f.close()
                        print "%s successfully loaded." % img_num
                        px_counter += 1
                        continue
                    except e:
                        print "error occurred", e
                        continue
                else:
                    print "can\'t get proxy, downloading stopped."
                    break
print "Done."