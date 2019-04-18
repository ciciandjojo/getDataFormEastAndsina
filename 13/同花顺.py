"""
    @Time:2019/4/18 11:02
    @Author: John Ma
"""

# coding:utf-8
from urllib import request, parse
import urllib
import http.cookiejar
from bs4 import BeautifulSoup
import requests
import json

def iwencai_From_10jqka( content ):
    mycookie = 'PHPSESSID=c0e068351fcc1411843aa1b4c8dd998c; ' \
               'cid=c0e068351fcc1411843aa1b4c8dd998c1555556464; ' \
               'ComputerID=c0e068351fcc1411843aa1b4c8dd998c1555556464; ' \
               'iwencaisearchquery=%E5%8C%97%E7%A7%91%E7%91%9E%E5%A3%B0; ' \
               'other_uid=Ths_iwencai_Xuangu_1e9ssn8vzue4xfihe9i4gkjl5fh0xe7z; ' \
               'other_uname=0su6vcs4ny; ' \
               'v=Apsw4qZJQ5qDsb9uZyrDFjvfKvQGcK9yqYRzJo3YdxqxbLViFUA_wrlUA3ee'

    content_code = urllib.request.quote(content)  # 解决中文编码的问题
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
               "Referer": "http://www.iwencai.com/search?typed=0&preParams=&ts=1&f=1&qs=result_tab&selfsectsn=&querytype=&bgid=&sdate=&edate=&searchfilter=&tid=news&w=" + content_code,
               "cookie" : mycookie,
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36', }

    # 上市股票地址
    target_url = 'http://www.iwencai.com/search?typed=0&preParams=&ts=1&f=1&qs=result_tab&selfsectsn=&querytype=&bgid=&sdate=&edate=&searchfilter=&tid=news&w=' + content_code
    req = requests.get(url=target_url, headers=headers)
    html = req.text
    page_bf = BeautifulSoup(html, 'lxml')
    for page_bf_itme in page_bf.select('.listcontian .s_r_box'):
        print(page_bf_itme)
        print(page_bf_itme.select('.s_r_blue_title a .title_word')[0].text)
        # print()

if __name__ == "__main__":
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')  # 改变标准输出的默认编码
    iwencai_From_10jqka("平安银行")