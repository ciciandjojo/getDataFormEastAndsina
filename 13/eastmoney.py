from urllib import request,parse
import urllib
import http.cookiejar
from bs4 import BeautifulSoup
import requests
import json

def eastmoney_text_get():
    content = '北科瑞声'

    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', }

    content_code = urllib.request.quote(content)  #解决中文编码的问题

    # 上市股票地址
    target_url = 'http://api.so.eastmoney.com/bussiness/Web/GetSearchList?type=20&pageindex=1&pagesize=10&keyword=' + content_code
    req = requests.get(url=target_url)
    req.encoding = 'utf-8'
    html = req.text

    data = json.loads(html)

    if data['IsSuccess']:
        # 循环输出所有的Data元素
        for i in range(0, len(data['Data'])):
            #文章的标题
            Art_Title = data['Data'][i]['Art_Title']

            #文章的地址
            Art_Url = data['Data'][i]['Art_Url']

            # 数据创建的时间
            Art_CreateTime = data['Data'][i]['Art_CreateTime']

            # 获取数据并且整理文本信息
            NoticeContent = ''
            for item in data['Data'][i]['Art_Content'].replace('\u003cem\u003e', '').replace('\u003c/em\u003e', '').splitlines():
                NoticeContent += ' '.join(item.split()) + ' '


