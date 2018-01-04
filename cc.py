# -*- coding: utf-8 -*-
"""
just for fun ...

This is a temporary script file.
"""
import tushare as ts
import os, sys, time
from threading import Thread

import pandas as pd
import numpy as np
from matplotlib.dates import date2num
from datetime import datetime, timedelta
from pprint import pprint
import xpinyin
import random


def test():
    for i in range(99):
        da1 = ts.get_realtime_quotes('300443')
        print(da1)
        time.sleep(2)

def test2():
    for i in range(1):
        da1 = ts.get_realtime_quotes('300443')
        print(da1['price'][0])
        print(((da1['price'][1]-da1['pre_close'][1])/da1['pre_close'][1])*100)
        # print(da1)
        time.sleep(2)

def getData():
    da1 = ts.get_today_all()
    da1.to_csv('jj.csv')

def testPandas():
    s = pd.Series([1,2,3,])

    dates = pd.date_range('20120101',periods=6)

    df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('ABCD'))

    ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
    ts = ts.cumsum()
    print(len(df))
    print(df.describe())
    print(df['A'].mean())
    print(df)

def testData():
    data = pd.read_excel('data.xlsx')
    data['code'] = data['code'].map(lambda x:('%06d'%x))

    data = data[data.amount > 0]
    data1 = data.sort_values(by= 'changepercent', ascending=False)

    cc = data.loc[:, ['code', 'name']]
    p = xpinyin.Pinyin()

    cc['py'] = cc['name'].map(lambda x:(''.join(p.get_initials(x, '').split())))

    # aa = [''.join(p.get_initials(x, '').split()) for x in data['name']]

    # cc = pd.merge(cc, bb, left_index=True, how='left')
    # cc = cc.append(bb, ignore_index = True)

    print(cc)


class cc:

    def __init__(self):
        self.myIndex = pd.DataFrame()
        self.__buildStockKey()


    def __buildStockKey(self):
        '''获取A股所有股票的代码和名称'''

        # 获取A股所有股票的基本信息
        try:
            data = ts.get_stock_basics()
        except:
            data = pd.read_excel(self.__getTempPath('stockCodes.xlsx'))

        if type(data) != pd.core.frame.DataFrame:
            print("Get stock basice info from xlsx")
            self.stockKey = None
            return
        self.stockKey = pd.DataFrame(columns=['code', 'name', 'py'])

        p = xpinyin.Pinyin()
        dd = data.loc[:,['name']]
        dd = dd.reset_index()
        dd['py'] = dd['name'].map(lambda x: (''.join(p.get_initials(x, '').split())))
        dd['name'] = dd['name'].map(lambda x: (''.join(x.split())))
        # dd['code'] = dd['code'].map(lambda x: ('%06d'%(int(x))))

        for i in dd.index:
            dd.loc[i, 'tip'] = '%s [%s(%s)]'%(dd.loc[i,'code'], dd.loc[i, 'name'], dd.loc[i, 'py'])

        dd.to_excel(self.__getTempPath('stockCodes.xlsx'))

        # 保存A股股票代码名称
        self.stockKey = dd

    def getIndexQuote(self):
        '''获取A股大盘指数的实时行情'''

        try:
            realData = ts.get_index()
            return realData
        except Exception as e:
            print(e)
            return None



    def getTodayAll(self):
        '''获取A股所有股票的实时市场数据'''
        # timesp = time.strftime('%H:%M:%S', time.localtime())

        try:
            if True:
                realData = ts.get_today_all()
                # realData.to_csv('./cc/data2.csv')
                realData.to_excel(self.__getTempPath('stcokTodayAll.xlsx'))
            else:
                realData = pd.read_excel(self.__getTempPath('stcokTodayAll.xlsx'), encoding='gbk')

        except Exception as e:
            print(e)
            return None
        return realData

    def getRealtimeQuote(self, code=None):
        '''获取输入代码的实时市场数据'''
        try:
            msg = ts.get_realtime_quotes(code)
            if type(msg) != pd.core.frame.DataFrame:
                return None
            lastPrice = float(msg.loc[0, 'price'])
            preClosePrice = float(msg.loc[0, 'pre_close'])
            try:
                msg['changePerPrice'] = round((lastPrice - preClosePrice)/preClosePrice, 4)
            except Exception as err:
                msg['changePerPrice'] = 0
        except Exception as e:
            print(e)
            return None

        return msg


    def getMyIndex(self):
        '''计算自定义市场实时数据指标'''

        data = self.getTodayAll()
        timeSp = time.strftime('%H:%M:%S', time.localtime())

        if data is None:
            return None

        realData = data[data.amount > 0]
        cun = len(realData)
        ##上涨家数
        tmp = realData[realData.changepercent > 0]
        up_cun = len(tmp)
        up_mean_per = tmp['changepercent'].mean()
        ##下跌家数
        tmp = realData[realData.changepercent < 0]
        down_cun = len(tmp)
        down_mean_per = tmp['changepercent'].mean()       

        ##涨停家数
        tmp = realData[realData.trade >= round(realData.settlement*1.1, 2)]
        top_cun = len(tmp)
        ## 真实涨停家数(非一字涨停)
        tmp = tmp[(tmp.low < tmp.trade) & (tmp.changepercent < 15)]
        top_cun_real = len(tmp)

        ##跌停家数
        tmp = realData[realData.trade <= round(realData.settlement*0.9, 2)]
        bom_cun = len(tmp)

        ##换手率排名前50
        turnoverratio = realData.sort_values(by= 'turnoverratio', ascending=False).head(50)
        ##换手率排名前50中上涨的家数
        turnoveration_50_cun = len(turnoverratio[turnoverratio.changepercent > 0])
        ##换手率排名前50平均增幅
        tmp = turnoverratio[turnoverratio.changepercent>0]
        turnoveration_50_up_mean_per =tmp['changepercent'].mean()
        ##换手率排名前50平均跌幅
        tmp = turnoverratio[turnoverratio.changepercent<0]
        turnoveration_50_down_mean_per =tmp['changepercent'].mean()

        ##换手率排名前100
        turnoverratio = realData.sort_values(by= 'turnoverratio', ascending=False).head(100)
        ##换手率排名前100中上涨的家数
        turnoveration_100_cun = len(turnoverratio[turnoverratio.changepercent > 0])
        ##换手率排名前100平均增幅
        tmp = turnoverratio[turnoverratio.changepercent>0]
        turnoveration_100_up_mean_per =tmp['changepercent'].mean()
        ##换手率排名前100平均跌幅
        tmp = turnoverratio[turnoverratio.changepercent<0]
        turnoveration_100_down_mean_per =tmp['changepercent'].mean()


        val = {'time':timeSp,
               'all_cun':[cun],
               'up_cun' :[up_cun],
               'top_cun':[top_cun],
               'bom_cun':[bom_cun],
               'turnoveration_50_cun':[turnoveration_50_cun],
               'turnoveration_100_cun':[turnoveration_100_cun],
               'up_rg': random.sample(range(0,100),1),
               'up_rg2': random.sample(range(0,100),1),
               # 'up_rg': [round(up_cun*100/cun, 2)],
               # 'up_rg2': [turnoveration_cun]
               }
        dd = pd.DataFrame(val)
        self.myIndex = self.myIndex.append(dd ,ignore_index = True)
        val = {
               'all_cun': [cun, '总数 '],
               'bom_cun': [bom_cun, '跌停家数'],
               'time'   : [timeSp, '时间'],
               'up_cun': [up_cun, '上涨家数'],
               'top_cun': [top_cun, '涨停家数'],
               'turnoveration_50_cun': [turnoveration_50_cun, '换手率前50 上涨家数'],
               'turnoveration_100_cun': [turnoveration_100_cun, '换手率前100 上涨家数'],

               '0': ['市场赚钱效应', '%0.2f%%'%(round(up_cun*100/cun, 2)), '平均涨跌幅(%0.2f%% :%0.2f%%)\n涨%d 跌%d'%(up_mean_per,down_mean_per,up_cun, down_cun)],
               '1': ['涨跌停比', '%d : %d'%(top_cun, bom_cun), '真实涨停%d'%(top_cun_real)],
               '2': ['高换手50效应','%d%%'%(turnoveration_50_cun), '平均涨跌幅(%0.2f%% :%0.2f%% )'%(turnoveration_50_up_mean_per,turnoveration_50_down_mean_per)],
               '3': ['高换手100效应','%d%%'%(turnoveration_100_cun), '平均涨跌幅(%0.2f%% :%0.2f%% )'%(turnoveration_50_up_mean_per,turnoveration_100_down_mean_per)]
               }
        return val

    # ----------------------------------------------------------------------
    def __getTempPath(self, name):
        """获取存放临时文件的路径"""
        tempPath = os.path.join(os.getcwd(), 'temp')
        if not os.path.exists(tempPath):
            os.makedirs(tempPath)
        path = os.path.join(tempPath, name)
        return path

    def dispMyIndex(self):
        print(self.myIndex)
        dd = self.myIndex.mean()
        print(dd)
        # self.myIndex.to_excel('./cc/myIndex.xlsx')

if __name__ == '__main__':
    test = cc()
    test.getMyIndex()
    time.sleep(5)
    test.dispMyIndex()
    # testPandas()