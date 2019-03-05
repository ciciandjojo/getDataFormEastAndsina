# -*- coding: utf-8 -*-
"""
    @Time:2019/3/4 14:55
    @Author: John Ma
"""

import time

def timeToTimestamp(format_time):
    # 格式化时间
    format_time = format_time

    # 时间
    ts = time.strptime(format_time, "%Y-%m-%d %H:%M:%S")
    #time.struct_time(tm_year=2017, tm_mon=3, tm_mday=16, tm_hour=18, tm_min=35, tm_sec=10, tm_wday=3, tm_yday=75, tm_isdst=0)

    # 格式化时间转时间戳
    print(time.mktime(ts))

def timestampToTime(now):
    import time
    # 时间戳
    now = now
    int(now)
    tl = time.localtime(now)
    # 格式化时间
    format_time = time.strftime("%Y-%m-%d %H:%M:%S", tl)
    print(format_time)

if __name__ == "__main__":

    format_time = time.strftime("%Y-%m-%d", time.localtime())
    ts = time.strptime(format_time + ' 00:00:00', "%Y-%m-%d %H:%M:%S")
    print(int(time.mktime(ts)))

    timestampToTime(1551693132)