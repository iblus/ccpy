# encoding: UTF-8

import os
import shelve
from collections import OrderedDict
from datetime import datetime

from ccFunction import getTempPath
from cc import cc
from ccObject import CCIndexData, CCTickData
from eventType import *
from eventEngine import Event, EventEngine2
import pandas as pd


########################################################################
class MainEngine(object):
    """主引擎"""

    # ----------------------------------------------------------------------
    def __init__(self, eventEngine):
        """Constructor"""
        # 记录今日日期
        self.todayDate = datetime.now().strftime('%Y%m%d')

        # 绑定事件引擎
        self.eventEngine = eventEngine
        self.eventEngine.start()

        # 创建数据引擎
        self.dataEngine = TickEngine(self.eventEngine)

        self.allStockList = self.dataEngine.cc.stockKey


    # ----------------------------------------------------------------------
    def exit(self):
        """退出程序前调用，保证正常退出"""

        # 停止事件引擎
        self.dataEngine.exit()
        self.eventEngine.stop()


########################################################################
class TickEngine(object):
    """实时行情引擎"""
    contractFileName = 'SelfStockCode.cc'
    contractFilePath = getTempPath(contractFileName)

    # ----------------------------------------------------------------------
    def __init__(self, eventEngine):
        """Constructor"""
        self.eventEngine = eventEngine

        # 用于计算获取自定义指数事件引擎，因通过网络获取A股全部数据需要较长事件，故单独分配个引擎
        self.eventEngineSelfIndex = EventEngine2()
        self.eventEngineSelfIndex.register(EVENT_GET_SELF_INDEX_TICK, self.getSelfIndexTick)
        self.eventEngineSelfIndex.start(False)

        #获取A股行情接口
        self.cc = cc()

        # 保存自选股票代码的列表
        self.stockCodeList = []

        # 读取保存在硬盘的自选股票代码
        self.loadStockCodeList()

        # 配置自选股和大盘指数更新频率
        self.selfStockTickTrigger = 3   #3秒更新一次
        self.selfStockTickCount = self.selfStockTickTrigger

        #配置自定义指标更新频率

        self.selfIndexTickTrigger = 60  #60秒更新一次

        self.selfIndexTickCount = self.selfIndexTickTrigger

        # 注册事件监听
        self.registerEvent()

    def exit(self):
        """关闭相关事件线程"""
        self.eventEngineSelfIndex.stop()

    # ----------------------------------------------------------------------
    def addStockCodeList(self, event):
        """添加自选股"""
        stock = event.dict_['data']
        if stock not in self.stockCodeList:
            self.stockCodeList.append(stock)

    # ----------------------------------------------------------------------
    def removeStockCodeList(self, event):
        """去除自选股"""
        stock = event.dict_['data']
        if stock in self.stockCodeList:
            self.stockCodeList.remove(stock)

    # ----------------------------------------------------------------------
    def getStockListTick(self, event=None):
        """获取大盘指数和自选股的实时行情"""

        # 获取大盘指数的实时行情
        indexList =['000001',   #上证指数
                    '000300',   #沪深300
                    '399606',   #创业板
                    ]

        indexTick = self.cc.getIndexQuote()
        if indexTick is not None:
            indexTick = indexTick[indexTick['code'].isin(indexList)]
            indexTick = indexTick.reset_index()
            indexMsg = ''
            for n,stock in enumerate(indexList):
                indexMsg += u'{}: {}%  '.format(indexTick.loc[n,'name'], indexTick.loc[n, 'change'])

            outTick = CCIndexData()
            outTick.symbol = '000001'
            outTick.name = indexMsg + datetime.now().strftime('%Y.%m.%d..%H:%M:%S')

            event = Event(EVENT_UPDATE_STATUS_BAR)
            event.dict_['data'] = outTick
            self.eventEngine.put(event)


        # 获取自选股的实时行情
        if len(self.stockCodeList) == 0:
            return None

        for n,stock in enumerate(self.stockCodeList):
            tick = self.cc.getRealtimeQuote(stock)
            if tick is None:
                return None

            outTick = CCTickData()
            outTick.symbol = tick.loc[0, 'code']
            outTick.name = tick.loc[0,'name']
            outTick.lastPrice = round(float(tick.loc[0,'price']),2)
            outTick.changePerPrice = tick.loc[0,'changePerPrice']
            outTick.time = tick.loc[0,'time']
            # 发送个股实时行情事件
            event = Event(EVENT_SELF_STOCK_TICK)
            event.dict_['data'] = outTick
            self.eventEngine.put(event)


    # ----------------------------------------------------------------------
    def getSelfIndexTick(self, event=None):
        """获取自定义指标实时行情"""

        readData = self.cc.getMyIndex()
        if readData is None:
            return
        # 显示时间
        outTickTime = CCIndexData()
        outTickTime.symbol = 'Time'
        outTickTime.name = readData['time'][0]
        outTickTime.lastPrice = ''
        outTickTime.tip = ''
        # print(outTick.tip)
        event = Event(EVENT_SELF_INDEX_TICK)
        event.dict_['data'] = outTickTime
        self.eventEngine.put(event)

        selfIndexList = ['M0','M1','M2','M3']
        for n,index in enumerate(selfIndexList):
            outTick = CCIndexData()
            outTick.symbol = index
            outTick.name = readData[str(n)][0]
            outTick.lastPrice = readData[str(n)][1]
            outTick.tip  = readData[str(n)][2]
            # print(outTick.tip)
            event = Event(EVENT_SELF_INDEX_TICK)
            event.dict_['data'] = outTick
            self.eventEngine.put(event)


    # ----------------------------------------------------------------------
    def saveSelfStockList(self):
        """保存自选股列表到硬盘"""
        pass


    # ----------------------------------------------------------------------
    def loadStockCodeList(self):
        """从硬盘读取自选股票代码"""

    # ----------------------------------------------------------------------
    def updateTick(self, event):
        """更新行情数据"""

        # 更新自选股和大盘指数行情数据
        self.selfStockTickCount += 1
        if self.selfStockTickCount >= self.selfStockTickTrigger:
            self.selfStockTickCount = 0
            self.getStockListTick()

        # 更新自定义指标数据
        self.selfIndexTickCount += 1
        if self.selfIndexTickCount >= self.selfIndexTickTrigger:
            self.selfIndexTickCount = 0

            event = Event(EVENT_GET_SELF_INDEX_TICK)
            event.dict_['data'] = None
            self.eventEngineSelfIndex.put(event, False)

    # ----------------------------------------------------------------------
    def registerEvent(self):
        """注册事件监听"""

        self.eventEngine.register(EVENT_TIMER, self.updateTick)
        self.eventEngine.register(EVENT_SELF_STOCK_ADD, self.addStockCodeList)
        self.eventEngine.register(EVENT_SELF_STOCK_REMOVE, self.removeStockCodeList)
