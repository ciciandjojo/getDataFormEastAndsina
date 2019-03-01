# -*- coding:UTF-8 -*-
import pymysql
import requests
import json
import re
from bs4 import BeautifulSoup

if __name__ == '__main__':
    # 打开数据库连接:host-连接主机地址,port-端口号,user-用户名,passwd-用户密码,db-数据库名,charset-编码
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='1', db='financialdata',
                           charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = conn.cursor()

    # 主要财务指标
    cwzb_dict = {'EPS': '基本每股收益', 'EPS_DILUTED': '摊薄每股收益', 'GROSS_MARGIN': '毛利率',
                 'CAPITAL_ADEQUACY': '资本充足率', 'LOANS_DEPOSITS': '贷款回报率', 'ROTA': '总资产收益率',
                 'ROEQUITY': '净资产收益率', 'CURRENT_RATIO': '流动比率', 'QUICK_RATIO': '速动比率',
                 'ROLOANS': '存贷比', 'INVENTORY_TURNOVER': '存货周转率', 'GENERAL_ADMIN_RATIO': '管理费用比率',
                 'TOTAL_ASSET2TURNOVER': '资产周转率', 'FINCOSTS_GROSSPROFIT': '财务费用比率', 'TURNOVER_CASH': '销售现金比率',
                 'YEAREND_DATE': '报表日期'}

    # 利润表
    lrb_dict = {'TURNOVER': '总营收', 'OPER_PROFIT': '经营利润', 'PBT': '除税前利润',
                'NET_PROF': '净利润', 'EPS': '每股基本盈利', 'DPS': '每股派息',
                'INCOME_INTEREST': '利息收益', 'INCOME_NETTRADING': '交易收益', 'INCOME_NETFEE': '费用收益', 'YEAREND_DATE': '报表日期'}

    # 资产负债表
    fzb_dict = {
        'FIX_ASS': '固定资产', 'CURR_ASS': '流动资产', 'CURR_LIAB': '流动负债',
        'INVENTORY': '存款', 'CASH': '现金及银行存结', 'OTHER_ASS': '其他资产',
        'TOTAL_ASS': '总资产', 'TOTAL_LIAB': '总负债', 'EQUITY': '股东权益',
        'CASH_SHORTTERMFUND': '库存现金及短期资金', 'DEPOSITS_FROM_CUSTOMER': '客户存款',
        'FINANCIALASSET_SALE': '可供出售之证券', 'LOAN_TO_BANK': '银行同业存款及贷款',
        'DERIVATIVES_LIABILITIES': '金融负债', 'DERIVATIVES_ASSET': '金融资产', 'YEAREND_DATE': '报表日期'}

    # 现金流表
    llb_dict = {
        'CF_NCF_OPERACT': '经营活动产生的现金流', 'CF_INT_REC': '已收利息', 'CF_INT_PAID': '已付利息',
        'CF_INT_REC': '已收股息', 'CF_DIV_PAID': '已派股息', 'CF_INV': '投资活动产生现金流',
        'CF_FIN_ACT': '融资活动产生现金流', 'CF_BEG': '期初现金及现金等价物', 'CF_CHANGE_CSH': '现金及现金等价物净增加额',
        'CF_END': '期末现金及现金等价物', 'CF_EXCH': '汇率变动影响', 'YEAREND_DATE': '报表日期'}

    # 总表
    table_dict = {'cwzb': cwzb_dict, 'lrb': lrb_dict, 'fzb': fzb_dict, 'llb': llb_dict}

    # 请求头
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.8',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36', }

    # 上市股票地址
    target_url = 'http://quotes.money.163.com/hkstock/cwsj_00700.html'
    req = requests.get(url=target_url, headers=headers)
    req.encoding = 'utf-8'
    html = req.text
    page_bf = BeautifulSoup(html, 'lxml')
    # 股票名称，股票代码
    name = page_bf.find_all('span', class_='name')[0].string
    code = page_bf.find_all('span', class_='code')[0].string
    code = re.findall('\d+', code)[0]
    # 打印股票信息
    print(name + ':' + code)
    print('')
    # 存储各个表名的列表
    table_name_list = []
    table_date_list = []
    each_date_list = []
    url_list = []
    # 表名和表时间
    table_name = page_bf.find_all('div', class_='titlebar3')
    for each_table_name in table_name:
        # 表名
        table_name_list.append(each_table_name.span.string)
        # 表时间
        for each_table_date in each_table_name.div.find_all('select', id=re.compile('.+1$')):
            url_list.append(re.findall('(\w+)1', each_table_date.get('id'))[0])
            for each_date in each_table_date.find_all('option'):
                each_date_list.append(each_date.string)
            table_date_list.append(each_date_list)
            each_date_list = []

    # 插入信息
    for i in range(len(table_name_list)):
        print('表名:', table_name_list[i])
        print('')

        # 获取数据地址
        url = 'http://quotes.money.163.com/hk/service/cwsj_service.php?symbol={}&start={}&end={}&type={}&unit=yuan'.format(
            code, table_date_list[i][-1], table_date_list[i][0], url_list[i])
        req_table = requests.get(url=url, headers=headers)
        value_dict = {}
        for each_data in req_table.json():
            value_dict['股票名'] = name
            value_dict['股票代码'] = code
            for key, value in each_data.items():
                if key in table_dict[url_list[i]]:
                    value_dict[table_dict[url_list[i]][key]] = value

            # print(value_dict)
            sql1 = """
            INSERT INTO %s (`股票名`,`股票代码`,`报表日期`) VALUES('%s','%s','%s')""" % (
            url_list[i], value_dict['股票名'], value_dict['股票代码'], value_dict['报表日期'])
            print(sql1)
            try:
                cursor.execute(sql1)
                # 执行sql语句
                conn.commit()
            except:
                # 发生错误时回滚
                conn.rollback()

            for key, value in value_dict.items():
                if key not in ['股票名', '股票代码', '报表日期']:
                    sql2 = """
                    UPDATE %s SET %s='%s' WHERE `股票名`='%s' AND `报表日期`='%s'""" % (
                    url_list[i], key, value, value_dict['股票名'], value_dict['报表日期'])
                    print(sql2)
                    try:
                        cursor.execute(sql2)
                        # 执行sql语句
                        conn.commit()
                    except:
                        # 发生错误时回滚
                        conn.rollback()
            value_dict = {}

    # 关闭数据库连接
    cursor.close()
    conn.close()
