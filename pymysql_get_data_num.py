# -*- coding: utf-8 -*-
"""
    @Time:2018/10/22 15:36
    @Author: John Ma
"""
import pymysql,os
import pandas as pd
from sqlalchemy import create_engine,Table,Column,Integer,String,MetaData,ForeignKey
from datetime import datetime
from sqlalchemy.types import NVARCHAR, Float, Integer


# pandas类型和sql类型转换
def map_types(df):
    dtypedict = {}
    for i, j in zip(df.columns, df.dtypes):
        if "object" in str(j):
            dtypedict.update({i: NVARCHAR(length=255)})
        if "float" in str(j):
            dtypedict.update({i: Float(precision=2, asdecimal=True)})
        if "int" in str(j):
            dtypedict.update({i: Integer()})
    return dtypedict

def get_data_num(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            L.append(str(file).split('.csv'))
    L_list = sum(L,[])
    while '' in L_list:
        L_list.remove('')
    print(L_list)
    return L_list


if __name__ == "__main__":
    # 连接设置 连接mysql 用户名ffzs 密码666 地址localhost：3306 database：stock
    engine = create_engine("mysql+mysqlconnector://root:1@localhost:3306/django")
    # 建立连接
    con = engine.connect()

    #将所有股票代码都放到
    L = get_data_num('Cement')

    for data_name in L:
        df = pd.read_csv('Cement/'+str(data_name)+'.csv', encoding='gbk', parse_dates=['日期'])
        dtypedict = map_types(df)
        # 通过dtype设置类型 为dict格式{“col_name”:type}
        print('开始将数据'+str(data_name)+'导入数据库.............')

        df.to_sql(name=str(data_name), con=con, if_exists='replace', index=False, dtype=dtypedict)
        print('数据'+str(data_name)+'导入完毕......................')