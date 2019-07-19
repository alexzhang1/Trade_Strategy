#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : get_quote.py
@Author: zhangwei
@Date  : 2019/6/28 9:25
@Desc  : 
"""

import requests
import sys
import numpy as np
import pandas as pd
import datetime as dt
from dateutil.parser import parse
import matplotlib.pyplot as plt
#import matplotlib.finance as mpf
import mpl_finance as mpf
from mpl_finance import candlestick_ohlc
from matplotlib.pylab import date2num



local_date = dt.datetime.today().strftime('%Y-%m-%d')

# 读实盘数据
# 功能：  实时读取新浪财经期货数据
# 参数:   请输入要读取的合约名称
# 返回值：以数组的形式返回


def read_real_future_data(future_code):
    # future_code ='M1909'
    # 从新浪财经读数据
    url_str = ('http://hq.sinajs.cn/list=' + future_code)
    r = requests.get(url_str)
    # 数据处理，保存在临时数组中
    b = list(r)
    #len(b)=2
    str1 = b[0].decode(encoding='gbk') + b[1].decode(encoding='gbk')
#    print("str1:",str1)
    str2 = str1.split(',')
#    print("str2:",str2)
    str3 = str2[0].split('_')[-1]
#    print("str3:",str3)
    str4 = str3.split('=')
#    print("str4:",str4)
    ##-------------------------------------------------------------------------
    ##  2018/7/5 shanghai tcy python版本
    ##f=[0,0,0,0,0,0,0,0]
    ##f[0]=str4[0]             #code
    ##f[1]=str4[1].strip('"')  #name
    ##f[2]=str2[17]  #date
    ##f[3]=str2[2]   #open
    ##f[4]=str2[3]   #high
    ##f[5]=str2[4]   #low
    ##f[6]=str2[6]   #close
    ##f[7]=str2[14]  #vol
    ##--------------------------------------------------------------------------
    ## numpy版本运行速度快
    dt = np.dtype([('code', 'S10'), ('name', 'U10'), ('date', 'datetime64[D]'), ('open', np.float32),
                   ('high', np.float32), ('low', np.float32), ('close', np.float32), ('vol', np.float32)])

    f = np.array([("", "", '1970-01-01', 0.0, 0.0, 0.0, 0.0, 0.0)], dtype=dt)
    f[0]['code'] = str4[0]  # code
    f[0]['name'] = str2[16]  # name
    f[0]['date'] = str2[17]  # date
    f[0]['open'] = str2[2]  # open
    f[0]['high'] = str2[3]  # high
    f[0]['low'] = str2[4]  # low
    f[0]['close'] = str2[6]  # close
    f[0]['vol'] = str2[14]  # vol
    # 测试程序
    ##    print('code name date,open,high,low,close,vol')
    ##    print(f)
    return f


'''
外盘期货行情
最新价,未知1,买价,卖价,最高价,最低价,行情时间,昨日结算价,开盘价,持仓量,未知2,未知3,交易日期,品种名称
var hq_str_hf_CAD="6018.700,,6019.000,6019.500,6075.000,6016.000,17:48:31,5993.000,6046.500,0.000,1,2,2019-07-01,伦铜";
var hq_str_hf_S="927.650,,927.750,928.000,934.250,926.750,18:02:04,923.000,933.750,325069.000,3,13,2019-07-01,美国大豆";
'''

# 读实盘数据
# 功能：  实时读取新浪财经外盘期货数据
# 参数:   请输入要读取的合约名称
# 返回值：以数组的形式返回


def read_real_external_future_data(future_code):
    # future_code ='CAD'
    # 从新浪财经读数据
    url_str = ('http://hq.sinajs.cn/list=hf_' + future_code)
    r = requests.get(url_str)
    # 数据处理，保存在临时数组中
    b = list(r)
    str1 = b[0].decode(encoding='gbk')
#    print("str1:",str1)
    str2 = str1.split(',')
#    print("str2:",str2)
    str3 = str2[0].split('_')[-1]
#    print("str3:",str3)
    str4 = str3.split('=')
#    print("str4:",str4)

    ## numpy版本运行速度快
    dt = np.dtype([('code', 'S10'), ('name', 'U10'), ('date', 'datetime64[D]'), ('open', np.float32),
                   ('high', np.float32), ('low', np.float32), ('close', np.float32), ('vol', np.float32)])

    f = np.array([("", "", '1970-01-01', 0.0, 0.0, 0.0, 0.0, 0.0)], dtype=dt)
    f[0]['code'] = str4[0]  # code
    f[0]['name'] = str2[13].replace('";\n','')  # name
    f[0]['date'] = str2[12]  # date
    f[0]['open'] = str2[8]  # open
    f[0]['high'] = str2[4]  # high
    f[0]['low'] = str2[5]  # low
    f[0]['close'] = str4[1].replace('"','')  # close
    f[0]['vol'] = str2[9]  # vol
    # 测试程序
    ##    print('code name date,open,high,low,close,vol')
    ##    print(f)
    return f


#内盘期货历史日线行情
def get_inner_futures_his_quote(future_code):
    
#    future_code = 'M1809'
    url_str = ('http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesDailyKLine?symbol=' +
    future_code)
    r = requests.get(url_str)
    r_json = r.json()
    r_lists = list(r_json)
#    print('future_code,date,open,high,low,close,vol')
    quote_list=[]
    quote_list.append(['future_code','date','open','high','low','close','vol'])
    #返回每项是[]list格式  
    for r_list in r_lists:
        r_list.insert(0, future_code)
        quote_list.append(r_list)
#    print(quote_list)
    df = pd.DataFrame(quote_list[1:], columns=quote_list[0])    
    return df


#外盘期货历史日线行情
def get_global_futures_his_quote(future_code):
    
#    future_code = 'CAD'
    url_str = ('http://stock2.finance.sina.com.cn/futures/api/json.php/GlobalFuturesService.getGlobalFuturesDailyKLine?symbol=' +
    future_code)
    r = requests.get(url_str)
    r_json = r.json()
    r_lists = list(r_json)
    quote_list=[]
    quote_list.append(['future_code','date','open','high','low','close','vol'])
    
    #返回每项是{}字典格式
    for r_dict in r_lists:
        tem = list(r_dict.values())
        tem.insert(0, future_code)
        quote_list.append(tem)
#    print(quote_list)
    
    df = pd.DataFrame(quote_list[1:], columns=quote_list[0])    
    return df

##测试程序：
##-----------------------------------------------------------------


#f = read_real_future_data('CU0')
#f = read_real_external_future_data('CAD')
#print('code,name,date,open,high,low,close,vol')
#print(f)

instrument = 'CU0'
inner_quote = get_inner_futures_his_quote(instrument)
csv_file_name = './quote_csv/InnerFuturesDailyKLine/' + instrument + '_' +  local_date + '.csv'
inner_quote.to_csv(csv_file_name, encoding='utf-8')


instrument = 'CAD'
inner_quote = get_global_futures_his_quote(instrument)
csv_file_name = './quote_csv/GlobalFuturesDailyKLine/' + instrument + '_' +  local_date + '.csv'
inner_quote.to_csv(csv_file_name, encoding='utf-8')
#get_global_futures_his_quote('CAD')




