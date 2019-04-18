from urllib import request,parse
import urllib
import requests
import json
from bs4 import BeautifulSoup

def eastmoney_text_get():
    content = '北科瑞声'

    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', }

    content_code = urllib.request.quote(content)  #解决中文编码的问题

    stockDict = {}
    # 上市股票地址
    target_url = 'https://gupiao.baidu.com/stock/sz300388.html'
    req = requests.get(url=target_url)
    req.encoding = 'utf-8'
    soupContent = BeautifulSoup(req.text, 'html.parser')


    if soupContent.select('.stock-bets'):
        soupContent_temp = soupContent.select('.stock-bets div')[0].select('strong')
        # 解析股票当日数据的头1
        for i in soupContent.select('.stock-bets h1 a'):
            stock_Name = i.text.replace("\n", "").replace("      ", "")
        now_price = soupContent_temp
        isOpenSell = soupContent.select('.stock-bets h1 span')[1].string
        pre_up = soupContent.select('.stock-bets div')[0].select('span')[0].string
        pre_up_precent = soupContent.select('.stock-bets div')[0].select('span')[1].string
        stockDict['stock_Name'] = stock_Name
        stockDict['now_price'] = now_price
        stockDict['pre_up'] = pre_up
        stockDict['pre_up_precent'] = pre_up_precent
        stockDict['isOpenSell'] = isOpenSell.split(' ')[0]
    print(now_price, pre_up, pre_up_precent)

    if soupContent.select('.bets-content'):
        # 解析股票当日数据的头2
        for i in soupContent.select('.bets-content'):
            stockKey = i.find_all('dt')
            stockValue = i.find_all('dd')
            for i in range(len(stockKey)):
                if stockKey[i].string == None:
                    stockDict['市盈率'] = stockValue[i].string
                else:
                    stockDict[stockKey[i].string] = stockValue[i].string.replace("\n", "").replace("      ", "")
    print(stockDict)


import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')  # 改变标准输出的默认编码
eastmoney_text_get()