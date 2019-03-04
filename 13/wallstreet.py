# -*- coding: utf-8 -*-
"""
    @Time:2019/3/4 9:47
    @Author: John Ma
"""
from urllib import request, parse
import urllib
import requests
import json
# coding:UTF-8
import time
import datetime

# 时间戳转化为时间
def timestampToTime(now):    # 时间戳
    now = now
    int(now)
    tl = time.localtime(now)
    # 格式化时间
    format_time = time.strftime("%Y-%m-%d %H:%M:%S", tl)
    print(format_time)

def wallstreet_text_get(timestamp):

    textAndTime = []

    block = ['global', 'blockchain', 'a_stock', 'us_stock', 'forex', 'commodity']

    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', }

    # 上市股票地址
    target_url = 'https://api-prod.wallstreetcn.com/apiv1/content/lives?channel=' + block[
        0] + '-channel&client=pc&cursor=' + str(timestamp)

    req = requests.get(url=target_url, headers=headers)
    print(req.status_code)
    req.encoding = 'utf-8'
    html = req.text

    wallstreet_all_message = json.loads(html)

    # print(wallstreet_all_message['data']['items'])
    if not wallstreet_all_message['data']['items']:
        print(wallstreet_all_message)
    else:
        for item in wallstreet_all_message['data']['items']:
            content_text = item['content_text']
            display_time = item['display_time']
            textAndTime.append(content_text)
            textAndTime.append(display_time)
            # print(content_text, display_time)
        # print('OK')
        # print(len(wallstreet_all_message['data']['items']))
    return textAndTime

# 定时去爬取数据
def timer(n):
    while True:
        get_one_day()
        time.sleep(n)

#
def get_one_day():

    textAndTime = []
    # 获取当前时间
    time_now = int(time.time())
    # 转换成localtime
    time_local = time.localtime(time_now)
    # 转换成新的时间格式(2016-05-09 18:59:20)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)

    timestamp = int(time.mktime(time_local))

    format_time = time.strftime("%Y-%m-%d", time.localtime())
    ts = time.strptime(format_time + ' 00:00:00', "%Y-%m-%d %H:%M:%S")

    # 先对获取一次数据，如果最后一位获取的时间比当天开始时间还小就继续获取，否则就继续获取
    time.localtime()
    textAndTime = wallstreet_text_get(timestamp)
    # print(textAndTime)
    if textAndTime:
        intoftext = textAndTime[len(textAndTime)-1]
        print(type(intoftext))
        print(type(int(time.mktime(ts))))
        while(int(intoftext) > int(time.mktime(ts))):
            textAndTime.extend(wallstreet_text_get(intoftext))
            intoftext = textAndTime[len(textAndTime)-1]
            print(intoftext)
    else:
        return textAndTime


if __name__ == "__main__":
    # 5s
    timer(1)

