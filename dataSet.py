# -*- coding: utf8 -*-
# coding: utf8
import urllib
import requests
from bs4 import BeautifulSoup
import re
import shutil
import os
import time

mainHeader = {}
mainHeader['Host'] = 'bsr.twse.com.tw'
mainHeader['Upgrade-Insecure-Requests'] = '1'
mainHeader['User-Agent'] = 'Mozilla/5.0 (Linux; Android 5.1.1; LG-D802 Build/LMY48Y) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.91 Mobile Safari/537.36'
mainHeader['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
mainHeader['Referer'] = 'http://bsr.twse.com.tw/bshtm/'
mainHeader['Accept-Encoding'] = 'gzip, deflate, sdch'
mainHeader['Accept-Language'] = 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4'
mainHeader['Cookie'] = 'ASP.NET_SessionId=xg3sdcpukh5cmtaazdjurgat'

i=0
while i < 20:
	i += 1
	response = requests.get("http://bsr.twse.com.tw/bshtm/bsMenu.aspx", headers=mainHeader)
	soup = BeautifulSoup(response.text, 'lxml')
	result = soup.find_all('img', src=re.compile('CaptchaImage.+'))

	response = requests.get("http://bsr.twse.com.tw/bshtm/"+result[0]['src'], headers=mainHeader, stream=True)

	if response.status_code == 200:
		print "http://bsr.twse.com.tw/bshtm/"+result[0]['src']
		with open(os.getcwd() + '/sample/' + str(int(time.time())) + '.jpg', 'wb') as f:
			response.raw.decode_content = True
			shutil.copyfileobj(response.raw, f)

	time.sleep(1)