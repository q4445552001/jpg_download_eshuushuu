#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import urllib2,os,time
from bs4 import BeautifulSoup

path = '/var/camera/image/'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'}
timesum = 0
tags = '28680'
dir = 'eshuushuu'

start = time.time() #時間開始

breakimg = 0
page = 1
print tags + ' Check Start'

if (os.path.isdir(path + dir) == False):
	os.system("mkdir " + path + dir)

os.chdir(path + dir)
stopimg = os.popen("ls |tail -n 1").read().split(".")[0]

while page <= 100 :
	url = 'http://e-shuushuu.net/search/results/?page=' + str(page) + '&tags=' + tags
	webside = urllib2.urlopen(urllib2.Request(url, None, headers), timeout=9999)
	soup = BeautifulSoup(webside, 'html.parser')
	links = soup.find_all('a',attrs={'class':'thumb_image'})

	img_urls = []
	img_ids = []
	
	#網址擷取
	for link in links:
		if link['href'].startswith('/images/'):
			img_urls.append(link['href'])
			img_ids.append(link['href'].split("-")[-1].split(".")[0])

	for img_url,img_id in zip(img_urls,img_ids):
		if stopimg != '' :
			if img_id <= stopimg :
				breakimg = 1
				#sys.exit()
				break
		os.system("wget -q -nc --show-progress -t 5 -T 30 -O " + img_id + "." + img_url.split(".")[-1] + " http://e-shuushuu.net" + img_url)

	if breakimg == 1 :
		break

	page += 1

end = time.time() #時間結束
timelog = end - start #花費時間
print tags + ' Check End. Time consuming : ' + str(timelog) + ' sec'

timesum = timesum + timelog
print "Time Sum : " + str(timesum/60) + ' min'