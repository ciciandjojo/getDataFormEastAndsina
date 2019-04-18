# -*- coding: utf-8 -*-
"""
    @Time:2019/4/17 9:35
    @Author: John Ma
"""

from pandas.core.frame import DataFrame
from urllib import request,parse
import urllib
import io
import json
import sys
from bs4 import BeautifulSoup
import requests
import cchardet

def zhengQuanZhiXing( stockname ):
    list_title = []
    list_time = []
    list_link = []
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip',
               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', }
    # content_code = urllib.request.quote(content)  #解决中文编码的问题
    # 上市股票地址
    target_url = 'http://news.stockstar.com/info/dstock.aspx?code=' + stockname
    req = requests.get(url=target_url, headers=headers)
    soupContent = BeautifulSoup(req.text, 'html.parser')

    if soupContent.select('.newslist_content'):
        for newslist_content in soupContent.select('.newslist_content'):
            for newslist_content_li in newslist_content.select('li'):
                if newslist_content_li.select('a'):
                    list_title.append(newslist_content_li.select('a')[0].text.replace('\n', '').replace('      ', '').replace('\r', ''))
                    list_link.append(newslist_content_li.select('a')[0]['href'])
                else:
                    list_time.append(newslist_content_li.text)

    dict_all = {"title" : list_title, "link": list_link, "time": list_time}
    data_all = DataFrame(dict_all)
    json_all = json.loads(data_all.to_json(orient='records', force_ascii=False))
    print(json_all)

def JinRongJie( stockname ):
    list_title = []
    list_time = []
    list_link = []
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip',
               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', }
    # content_code = urllib.request.quote(content)  #解决中文编码的问题
    # 上市股票地址
    target_url = 'http://so.jrj.com.cn/cse/search?q='+ stockname + '&click=1&s=5981575158355482147&nsid=1'
    req = requests.get(url=target_url, headers=headers)
    soupContent = BeautifulSoup(req.text, 'html.parser')
    if soupContent.select('.content-main'):
        for results_item in soupContent.select('.content-main .s0'):
            list_title.append(results_item.select('h3 a')[0].text.encode("iso-8859-1").decode('utf8'))
            list_link.append(results_item.select('h3 a')[0]['href'])
            list_time.append(results_item.select('.c-showurl')[0].text.split(' ')[1])

    dict_all = {"title" : list_title, "link": list_link, "time": list_time}
    data_all = DataFrame(dict_all)
    json_all = json.loads(data_all.to_json(orient='records', force_ascii=False))
    print(json_all)

def ZhongGuoShouSuo( stockname ):
    list_title = []
    list_time = []
    list_link = []
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip',
               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', }
    # content_code = urllib.request.quote(content)  #解决中文编码的问题
    # 上市股票地址
    target_url = 'http://news.chinaso.com/newssearch.htm?q=' + stockname
    req = requests.get(url=target_url, headers=headers)
    soupContent = BeautifulSoup(req.text, 'html.parser')
    if soupContent.select('.seResult'):
        for reItem in soupContent.select('.seResult .reItem'):
            list_title.append(reItem.select('h2 a')[0].text)
            list_link.append(reItem.select('h2 a')[0]['href'])
            list_time.append(reItem.select('.snapshot span')[0].text.split('\xa0')[0])
    dict_all = {"title" : list_title, "link": list_link, "time": list_time}
    data_all = DataFrame(dict_all)
    json_all = json.loads(data_all.to_json(orient='records', force_ascii=False))
    print(json_all)

def eastmoney( stockname ):
    list_title = []
    list_time = []
    list_link = []

    content_code = urllib.request.quote(stockname)  #解决中文编码的问题
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip',
               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
               "Referer": "http://so.eastmoney.com/news/s?keyword="+content_code,}
    # 上市股票地址
    target_url = 'http://api.so.eastmoney.com/bussiness/Web/GetSearchList?type=20&pageindex=1&pagesize=10&keyword='+ content_code +'&name=normal'
    req = requests.get(url=target_url, headers=headers)
    json_data = json.loads(req.text)

    if json_data['IsSuccess']:
        for json_data_Data in json_data['Data']:
            list_title.append(json_data_Data['Art_Title'].replace('<em>', '').replace('</em>', ''))
            list_link.append(json_data_Data['Art_Url'])
            list_time(json_data_Data['Art_CreateTime'].split(' ')[0])

    dict_all = {"title" : list_title, "link": list_link, "time": list_time}
    data_all = DataFrame(dict_all)
    json_all = json.loads(data_all.to_json(orient='records', force_ascii=False))
    print(json_all)

def cnfol( stockname ):
    list_title = []
    list_time = []
    list_link = []
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip',
               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', }
    # content_code = urllib.request.quote(content)  #解决中文编码的问题
    # 上市股票地址
    target_url = 'http://so.cnfol.com/cse/search?q=%E5%8C%97%E7%A7%91%E7%91%9E%E5%A3%B0&click=1&s=12596448179979580087&nsid=1'
    req = requests.get(url=target_url, headers=headers)
    soupContent = BeautifulSoup(req.text, 'html.parser')
    if soupContent.select('.s0'):
        for result_item in soupContent.select('.s0'):
            list_title.append(result_item.select('h3 a')[0].text.encode("iso-8859-1").decode('utf8'))
            list_link.append(result_item.select('h3 a')[0]['href'])
            list_time.append(result_item.select('.c-showurl')[0].text.split(' ')[1])
    dict_all = {"title" : list_title, "link": list_link, "time": list_time}
    data_all = DataFrame(dict_all)
    json_all = json.loads(data_all.to_json(orient='records', force_ascii=False))


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')  # 改变标准输出的默认编码
    cnfol('北科瑞声')