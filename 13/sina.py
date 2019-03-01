# -*- coding: utf-8 -*-
"""
    @Time:2019/2/22 9:55
    @Author: John Ma
"""
from urllib import request,parse
import urllib
import http.cookiejar
from bs4 import BeautifulSoup
import requests
import json
import time
# def eastmoney_text_get():
content = '北科瑞声'

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip',
           'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', }

import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030') #改变标准输出的默认编码

content_code = urllib.request.quote(content)  #解决中文编码的问题
# 上市股票地址
target_url = 'https://search.sina.com.cn/?country=usstock&q=%E5%8C%97%E7%A7%91%E7%91%9E%E5%A3%B0&name=%E5%8C%97%E7%A7%91%E7%91%9E%E5%A3%B0&t=&c=news&k=%E5%8C%97%E7%A7%91%E7%91%9E%E5%A3%B0&range=all&col=1_7&from=channel&&ie=gbk'
req = requests.get(url=target_url)
soupContent = BeautifulSoup(req.text, 'html.parser')

if soupContent.select('.box-result'):

    print(len(soupContent.select('.box-result')))
    #解析新闻子栏目
    for i in soupContent.select('.box-result'):
        # title
        # time.sleep(3)
        print(i.select('h2 a')[0].text)
        # time.sleep(1)
        #href
        print(i.select('a')[0]['href'])
        #fgray_time
        print(i.select('.fgray_time')[0].text)
        #content
        print(i.select('.content')[0].text)

# print(.decode('utf-8'))
