# -*- coding: utf-8 -*-
"""
    @Time:2019/3/4 9:47
    @Author: John Ma
"""
import requests
import json
import time
import sys
import io

# 时间转化为时间戳
def timeToTimestamp(format_time):
    # 格式化时间
    format_time = format_time
    # 时间
    ts = time.strptime(format_time, "%Y-%m-%d %H:%M:%S")
    # 格式化时间转时间戳
    return time.mktime(ts)

# 时间戳转化为时间
def timestampToTime(now):  # 时间戳
    now = now
    int(now)
    tl = time.localtime(now)
    # 格式化时间
    format_time = time.strftime("%Y-%m-%d %H:%M:%S", tl)
    return format_time

# 单次去获取数据    因为api的限制每次只能获取100条数据
def wallstreet_text_get(timestamp):
    textAndTime = []
    block = ['global', 'blockchain', 'a_stock', 'us_stock', 'forex', 'commodity']
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', }
    # 上市股票地址
    target_url = 'https://api-prod.wallstreetcn.com/apiv1/content/lives?channel=' + block[
        0] + '-channel&client=pc&cursor=' + str(timestamp-1)
    req = requests.get(url=target_url)
    req.encoding = 'utf-8'
    html = req.text
    wallstreet_all_message = json.loads(html)
    if not wallstreet_all_message['data']['items']:
        print('items没有数据')
    else:
        for item in wallstreet_all_message['data']['items']:
            content_text = item['content_text']
            display_time = timestampToTime(item['display_time'])
            textAndTime.append(content_text)
            textAndTime.append(display_time)
            # print(display_time)
    return textAndTime


# 定时去爬取数据
def timer():
    while True:
        get_one_day0 = get_one_day()
        if get_one_day0["all_message"]:
            return 1
        else:
            return 0

# 获取一天的所有信息   成功返回当天的      失败返回空
def get_one_day():
    textAndTime_oneDay = []
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
    # 再对已经获取的内容进行筛选只是当天的数据
    time.localtime()
    textAndTime_all = wallstreet_text_get(timestamp)
    if textAndTime_all:
        intoftext = int(timeToTimestamp(textAndTime_all[len(textAndTime_all) - 1]))
        while (intoftext > int(time.mktime(ts))):

            textAndTime_all.extend(wallstreet_text_get(intoftext))
            intoftext = int(timeToTimestamp(textAndTime_all[len(textAndTime_all) - 1]))

        textAndTime_all_2list = [textAndTime_all[i:i+2] for i in range(0,len(textAndTime_all), 2)]

        for pre in textAndTime_all_2list:
            pre_timestamp = timeToTimestamp(pre[1])
            if (int(pre_timestamp) > int(time.mktime(ts))):
                textAndTime_oneDay.extend(pre)
        textAndTime_oneDay_2list = [textAndTime_oneDay[i:i + 2] for i in range(0, len(textAndTime_oneDay), 2)]

        all_message_json = {}
        all_message_json["all_message"] = textAndTime_oneDay_2list
        # print(all_massage_json)
        return all_message_json
    else:
        all_message_json = {}
        all_message_json["all_message"] = textAndTime_all
        print(all_message_json)
        return all_message_json


if __name__ == "__main__":
    # 5s
    # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')  # 改变标准输出的默认编码

    while True:
        timer0 = timer()
        print('timer0: '+str(timer0))
        time.sleep(2)
