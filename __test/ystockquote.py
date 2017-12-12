# encoding='utf-8'
#
#  ystockquote : Python module - retrieve stock quote data from Yahoo Finance
#
#  Copyright (c) 2007,2008,2013,2016 Corey Goldberg (cgoldberg@gmail.com)
#
#  license: GNU LGPL
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.
#
#  Requires: Python 2.7/3.3+


__version__ = '0.2.5'  # NOQA


try:
    # py3
    from urllib.request import Request, urlopen
    from urllib.parse import urlencode
except ImportError:
    # py2
    from urllib2 import Request, urlopen
    from urllib import urlencode


def _request(symbol, stat):
    url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (symbol, stat)
    req = Request(url)
    resp = urlopen(req)
    content = resp.read().decode().strip()
    return content


def get_all(symbol):
    """
    Get all available quote data for the given ticker symbol.

    Returns a dictionary.
    """
    ids = \
        'ydb2r1b3qpoc1d1cd2c6t1k2p2c8m5c3m6gm7hm8k1m3lm4l1t8w1g1w4g3p' \
        '1g4mg5m2g6kvjj1j5j3k4f6j6nk5n4ws1xj2va5b6k3t7a2t615l2el3e7v1' \
        'e8v7e9s6b4j4p5p6rr2r5r6r7s7'
    values = _request(symbol, ids).split(',')
    return dict(
        dividend_yield=values[0],
        dividend_per_share=values[1],
        ask_realtime=values[2],
        dividend_pay_date=values[3],
        bid_realtime=values[4],
        ex_dividend_date=values[5],
        previous_close=values[6],
        today_open=values[7],
        change=values[8],
        last_trade_date=values[9],
        change_percent_change=values[10],
        trade_date=values[11],
        change_realtime=values[12],
        last_trade_time=values[13],
        change_percent_realtime=values[14],
        change_percent=values[15],
        after_hours_change_realtime=values[16],
        change_200_sma=values[17],
        todays_low=values[18],
        change_50_sma=values[19],
        todays_high=values[20],
        percent_change_50_sma=values[21],
        last_trade_realtime_time=values[22],
        fifty_sma=values[23],
        last_trade_time_plus=values[24],
        twohundred_sma=values[25],
        last_trade_price=values[26],
        one_year_target=values[27],
        todays_value_change=values[28],
        holdings_gain_percent=values[29],
        todays_value_change_realtime=values[30],
        annualized_gain=values[31],
        price_paid=values[32],
        holdings_gain=values[33],
        todays_range=values[34],
        holdings_gain_percent_realtime=values[35],
        todays_range_realtime=values[36],
        holdings_gain_realtime=values[37],
        fiftytwo_week_high=values[38],
        more_info=values[39],
        fiftytwo_week_low=values[40],
        market_cap=values[41],
        change_from_52_week_low=values[42],
        market_cap_realtime=values[43],
        change_from_52_week_high=values[44],
        float_shares=values[45],
        percent_change_from_52_week_low=values[46],
        company_name=values[47],
        percent_change_from_52_week_high=values[48],
        notes=values[49],
        fiftytwo_week_range=values[50],
        shares_owned=values[51],
        stock_exchange=values[52],
        shares_outstanding=values[53],
        volume=values[54],
        ask_size=values[55],
        bid_size=values[56],
        last_trade_size=values[57],
        ticker_trend=values[58],
        average_daily_volume=values[59],
        trade_links=values[60],
        order_book_realtime=values[61],
        high_limit=values[62],
        eps=values[63],
        low_limit=values[64],
        eps_estimate_current_year=values[65],
        holdings_value=values[66],
        eps_estimate_next_year=values[67],
        holdings_value_realtime=values[68],
        eps_estimate_next_quarter=values[69],
        revenue=values[70],
        book_value=values[71],
        ebitda=values[72],
        price_sales=values[73],
        price_book=values[74],
        pe=values[75],
        pe_realtime=values[76],
        peg=values[77],
        price_eps_estimate_current_year=values[78],
        price_eps_estimate_next_year=values[79],
        short_ratio=values[80],
    )


def get_dividend_yield(symbol):
    return _request(symbol, 'y')


def get_dividend_per_share(symbol):
    return _request(symbol, 'd')


def get_ask_realtime(symbol):
    return _request(symbol, 'b2')


def get_dividend_pay_date(symbol):
    return _request(symbol, 'r1')


def get_bid_realtime(symbol):
    return _request(symbol, 'b3')


def get_ex_dividend_date(symbol):
    return _request(symbol, 'q')


def get_previous_close(symbol):
    return _request(symbol, 'p')


def get_today_open(symbol):
    return _request(symbol, 'o')


def get_change(symbol):
    return _request(symbol, 'c1')


def get_last_trade_date(symbol):
    return _request(symbol, 'd1')


def get_change_percent_change(symbol):
    return _request(symbol, 'c')


def get_trade_date(symbol):
    return _request(symbol, 'd2')


def get_change_realtime(symbol):
    return _request(symbol, 'c6')


def get_last_trade_time(symbol):
    return _request(symbol, 't1')


def get_change_percent_realtime(symbol):
    return _request(symbol, 'k2')


def get_change_percent(symbol):
    return _request(symbol, 'p2')


def get_after_hours_change(symbol):
    return _request(symbol, 'c8')


def get_change_200_sma(symbol):
    return _request(symbol, 'm5')


def get_commission(symbol):
    return _request(symbol, 'c3')


def get_percent_change_200_sma(symbol):
    return _request(symbol, 'm6')


def get_todays_low(symbol):
    return _request(symbol, 'g')


def get_change_50_sma(symbol):
    return _request(symbol, 'm7')


def get_todays_high(symbol):
    return _request(symbol, 'h')


def get_percent_change_50_sma(symbol):
    return _request(symbol, 'm8')


def get_last_trade_realtime_time(symbol):
    return _request(symbol, 'k1')


def get_50_sma(symbol):
    return _request(symbol, 'm3')


def get_last_trade_time_plus(symbol):
    return _request(symbol, 'l')


def get_200_sma(symbol):
    return _request(symbol, 'm4')


def get_last_trade_price(symbol):
    return _request(symbol, 'l1')


def get_1_year_target(symbol):
    return _request(symbol, 't8')


def get_todays_value_change(symbol):
    return _request(symbol, 'w1')


def get_holdings_gain_percent(symbol):
    return _request(symbol, 'g1')


def get_todays_value_change_realtime(symbol):
    return _request(symbol, 'w4')


def get_annualized_gain(symbol):
    return _request(symbol, 'g3')


def get_price_paid(symbol):
    return _request(symbol, 'p1')


def get_holdings_gain(symbol):
    return _request(symbol, 'g4')


def get_todays_range(symbol):
    return _request(symbol, 'm')


def get_holdings_gain_percent_realtime(symbol):
    return _request(symbol, 'g5')


def get_todays_range_realtime(symbol):
    return _request(symbol, 'm2')


def get_holdings_gain_realtime(symbol):
    return _request(symbol, 'g6')


def get_52_week_high(symbol):
    return _request(symbol, 'k')


def get_more_info(symbol):
    return _request(symbol, 'v')


def get_52_week_low(symbol):
    return _request(symbol, 'j')


def get_market_cap(symbol):
    return _request(symbol, 'j1')


def get_change_from_52_week_low(symbol):
    return _request(symbol, 'j5')


def get_market_cap_realtime(symbol):
    return _request(symbol, 'j3')


def get_change_from_52_week_high(symbol):
    return _request(symbol, 'k4')


def get_float_shares(symbol):
    return _request(symbol, 'f6')


def get_percent_change_from_52_week_low(symbol):
    return _request(symbol, 'j6')


def get_company_name(symbol):
    return _request(symbol, 'n')


def get_percent_change_from_52_week_high(symbol):
    return _request(symbol, 'k5')


def get_notes(symbol):
    return _request(symbol, 'n4')


def get_52_week_range(symbol):
    return _request(symbol, 'w')


def get_shares_owned(symbol):
    return _request(symbol, 's1')


def get_stock_exchange(symbol):
    return _request(symbol, 'x')


def get_shares_outstanding(symbol):
    return _request(symbol, 'j2')


def get_volume(symbol):
    return _request(symbol, 'v')


def get_ask_size(symbol):
    return _request(symbol, 'a5')


def get_bid_size(symbol):
    return _request(symbol, 'b6')


def get_last_trade_size(symbol):
    return _request(symbol, 'k3')


def get_ticker_trend(symbol):
    return _request(symbol, 't7')


def get_average_daily_volume(symbol):
    return _request(symbol, 'a2')


def get_trade_links(symbol):
    return _request(symbol, 't6')


def get_order_book_realtime(symbol):
    return _request(symbol, 'i5')


def get_high_limit(symbol):
    return _request(symbol, 'l2')


def get_eps(symbol):
    return _request(symbol, 'e')


def get_low_limit(symbol):
    return _request(symbol, 'l3')


def get_eps_estimate_current_year(symbol):
    return _request(symbol, 'e7')


def get_holdings_value(symbol):
    return _request(symbol, 'v1')


def get_eps_estimate_next_year(symbol):
    return _request(symbol, 'e8')


def get_holdings_value_realtime(symbol):
    return _request(symbol, 'v7')


def get_eps_estimate_next_quarter(symbol):
    return _request(symbol, 'e9')


def get_revenue(symbol):
    return _request(symbol, 's6')


def get_book_value(symbol):
    return _request(symbol, 'b4')


def get_ebitda(symbol):
    return _request(symbol, 'j4')


def get_price_sales(symbol):
    return _request(symbol, 'p5')


def get_price_book(symbol):
    return _request(symbol, 'p6')


def get_pe(symbol):
    return _request(symbol, 'r')


def get_pe_realtime(symbol):
    return _request(symbol, 'r2')


def get_peg(symbol):
    return _request(symbol, 'r5')


def get_price_eps_estimate_current_year(symbol):
    return _request(symbol, 'r6')


def get_price_eps_estimate_next_year(symbol):
    return _request(symbol, 'r7')


def get_short_ratio(symbol):
    return _request(symbol, 's7')


def get_historical_prices(symbol, start_date, end_date):
    """
    Get historical prices for the given ticker symbol.
    Date format is 'YYYY-MM-DD'

    Returns a nested dictionary (dict of dicts).
    outer dict keys are dates ('YYYY-MM-DD')
    """
    params = urlencode({
        's': symbol,
        'a': int(start_date[5:7]) - 1,
        'b': int(start_date[8:10]),
        'c': int(start_date[0:4]),
        'd': int(end_date[5:7]) - 1,
        'e': int(end_date[8:10]),
        'f': int(end_date[0:4]),
        'g': 'd',
        'ignore': '.csv',
    })
    url = 'http://real-chart.finance.yahoo.com/table.csv?%s' % params
    req = Request(url)
    resp = urlopen(req)
    content = str(resp.read().decode('utf-8').strip())
    daily_data = content.splitlines()
    hist_dict = dict()
    keys = daily_data[0].split(',')
    for day in daily_data[1:]:
        day_data = day.split(',')
        date = day_data[0]
        hist_dict[date] = \
            {keys[1]: day_data[1],
             keys[2]: day_data[2],
             keys[3]: day_data[3],
             keys[4]: day_data[4],
             keys[5]: day_data[5],
             keys[6]: day_data[6]}
    return hist_dict
####################################################################
# end ystockquote
####################################################################

import struct
import requests

def get_last_avg(data, length):
    last = len(data)
    avg_ = 0
    if(last < (length)):
        avg_ = data[-1]
    else:
        for i in data[last-length:last]:
            avg_ =avg_ + i
        avg_ = avg_/length
    return avg_

def get_china_stock_individua_historical_prices(symbol, start_date, end_date):
    """
    Get china individual stock historical prices for the given ticker symbol.
    Date format is 'YYYYMMDD'

    Returns a nested dictionary (dict of dicts).
    outer dict keys are dates ('YYYYMMDD')
    """
    exchange = ".sh" if (int(symbol) // 100000 == 6) else ".sz"
    stockCode = symbol + exchange
    params = urlencode({
        's': stockCode,
        'a': int(start_date[4:6]) - 1,
        'b': int(start_date[6:8]),
        'c': int(start_date[0:4]),
        'd': int(end_date[4:6]) - 1,
        'e': int(end_date[6:8]),
        'f': int(end_date[0:4]),
        'g': 'd',
        'ignore': '.csv',
    })
    url = 'http://ichart.yahoo.com/table.csv?%s' % params
    print(url)
    try:
        #req = Request(url)
        #resp = urlopen(req)
        resp = open(r'table.csv','rb')
        content = str(resp.read().decode('utf-8').strip())
        daily_data = content.splitlines()
    except Exception as err:
        print(">>>>>> Exception: " + str(err))
        return None
    hist_dict = dict()
    keys = daily_data[0].split(',')
    print(keys)
    
    daily_value = [0]
    tabeList = ('id', 'open', 'high', 'low', 'close',  'amount', 'volume', 'adj_close', 'avg_5', 'avg_10')
    for which in range(-1,-len(daily_data)+1,-1):

        day = daily_data[which]
        day_data = day.split(',')
        tmp_data0 = day_data[0][0:4] + day_data[0][5:7] + day_data[0][8:10]
        date = int(tmp_data0)

        if(int(day_data[5]) != 0):
            daily_value.append(float(day_data[4]))
            avg_5  = get_last_avg(daily_value, 5)
            avg_10 = get_last_avg(daily_value, 10)
            avg_24 = get_last_avg(daily_value, 24)
            # print('data:%d close:%f real:%f 5:%f 10:%f 24:%f \n'%(int(date),float(day_data[4]),daily_value[-1], float(avg_5),float(avg_10),float(avg_24)))
            hist_dict[date] = \
                {'open': float(day_data[1]),
                 'high': float(day_data[2]),
                 'low': float(day_data[3]),
                 'close': float(day_data[4]),
                 'volume': float(day_data[5]),
                 'adj_close': float(day_data[6]),
                 'avg_5': avg_5,
                 'avg_10': avg_10,
                 'avg_24': avg_24,
                 'amount': 0,}

    return hist_dict

def getStockDataFromTXDFile(_code, _start, _end):
    '''
       get stock data from TXD
       _code: the code of stock, such as sz000001
       _start : the start date of stock that you want to look up
       _end   : the end date of stock that you want to look up

       struct TDSData_Day
        {
            unsigned long date;
            unsigned long open;
            unsigned long high;
            unsigned long low;
            unsigned long close;
            float amount;
            unsigned long vol;
            int reserv;
        };
    '''
    try:
        if (_code[0:2] == 'sh') :
            _file = 'F:/cc/table/vipdoc/sh/lday/' + str(_code) + '.day'
        else:
            _file = 'F:/cc/table/vipdoc/sz/lday/' + str(_code) + '.day' 

        ff = open(_file,'rb')
    except Exception as err:
        print(">>>>>> Exception: " + str(err))
        return None

    try:
        ss = ff.read()
        bb = dict()
        cc = dict()
        daily_value = list()
        DIF_value = list()
        for i in range(int(len(ss)/(4*8))):
            dd  = ss[i*32:i*32+32]
            tmp = struct.unpack('LLLLLfLi',dd)
            daily_value.append(tmp[4]/100.0)

            avg_12 = get_last_avg(daily_value, 12)
            avg_26 = get_last_avg(daily_value, 26)
            DIF    = avg_12 - avg_26
            DIF_value.append(DIF)
            DEM    = get_last_avg(DIF_value, 9)

            avg_5  = get_last_avg(daily_value, 5)
            avg_10 = get_last_avg(daily_value, 10)
            avg_24 = get_last_avg(daily_value, 24)
            if (int(tmp[0]) < int(_start)) or (int(tmp[0]) > int(_end)):
                continue
            bb[str(tmp[0])] = {
                'open':float(tmp[1]/100.0),
                'high':float(tmp[2]/100.0),
                'low':float(tmp[3]/100.0),
                'close':float(tmp[4]/100.0),
                'amount':float(tmp[5]),
                'volume':float(tmp[6]),
                'adj_close':0,
                'macd_dif':float(int(DIF*1000)/1000),
                'macd_dem':float(int(DEM*1000)/1000),
                'avg_5':float(int(avg_5*1000)/1000), 
                'avg_10':float(int(avg_10*1000)/1000),
                'avg_24':float(int(avg_24*1000)/1000)}
        ff.close()
        cc[str(_code)] = bb
        return cc
    except Exception as err:
        print(">>>>>> Exception: " + str(err))
        return None


def getStockList(_file):
    '''获取A股股票代码列表
       返回字典:key=code,
               value= name
    '''
    try:
        fb = open(_file)
        tt = fb.readlines()
    
        dd = dict()
        for ff in tt:
            mm = ((ff).rstrip()).split('\t')
            mm[0] = (mm[0]).lower()
            dd[mm[0]] = mm[1]
        print('the amount of all stock is : ' + str(len(dd)))
        fb.close()
        dd['sh000001'] = '上证指数'
        dd['sz399001'] = '深证成指'
        dd['sh000300'] = '沪深300'
        dd['sz399006'] = '创业板指'
        return dd
    except Exception as err:
        print(">>>>>> Exception: " + str(err))
        return None

def getAllStockFromTDXandDoIt(_start, _end):
    '''从通达信下载的数据中获取A股所有股票的历史交易数据,返回字典
    _start   : 统计的起始时间
    _end     : 统计的终止时间
    '''
    jj = getStockList('list.txt')
    if jj == None:
        return None

    allStockData = dict()
    stockList = sorted(jj.keys())
    disp_i   = 0
    disp_tmp = 0

    indexdata = getStockDataFromTXDFile('sh000001', _start, _end)
    _indexdata = indexdata['sh000001']

    for which in stockList[1:]:
        try:
            stockdata = getStockDataFromTXDFile(str(which), _start, _end)
            if stockdata == None:
                print('No data of %s !'%(which))
                continue
            #allStockData[str(which)] = stockdata
            _stockdata = stockdata[str(which)]
            a = cal_vga_5_10(_stockdata, str(which), jj[which])
            #stock_sqlite.creatStatDB('h5_10.db',a)
            #print('      %2d  %s [%s] lv: %0.2f%s  freq:%d'%(a['isout'], a['code'], 'name', (a['h5_10'])*100, '%', a['freq']))
            
            a = cal_vga_5_10_index(_stockdata, _indexdata, str(which), jj[which])
            #stock_sqlite.creatStatDB('h5_10_index.db',a)
            print('Index %2d  %s [%s] lv: %0.2f%s  freq:%d'%(a['isout'], a['code'], 'name', (a['h5_10'])*100, '%', a['freq']))
            
            allStockData[str(which)] = a

            disp_i += 1
            if int(disp_i/(len(stockList))*100) != disp_tmp : 
                disp_tmp = int(disp_i/(len(stockList))*100)
                #print('complete percent: %d%s'%(disp_tmp,'%'))
            print('%4d%s %4d :: %s [%s]'%(disp_tmp, '%', disp_i,which,jj[which]), end="\r")
        except Exception as e:
            print(">>>>>> Exception: " + str(e))
            continue

    print("all stock has been into dict !!!")
    return allStockData

###############################################################
import os, io, sys, re, time, json, base64
import webbrowser, urllib.request
import decimal

period_All_List = [
                    "min",      #分时线
                    "daily",    #日K线
                    "weekly",   #周K线
                    "monthly"   #月K线
                  ]
period_min = period_All_List[0]
period_daily = period_All_List[1]

ChinaStockIndexList = [
    "000001", # sh000001 上证指数
    "399001", # sz399001 深证成指
    "000300", # sh000300 沪深300
    "399006", # sz399006 创业板指

]
ChinaStockIndividualList = [
    "002292", #奥飞动漫
]

WorldStockIndexList = [
    {'code':"000001", 'yahoo':"000001.SS",'name':{'chinese':"中国上证指数", 'english':"CHINA SHANGHAI COMPOSITE INDEX"}},
    {'code':"399001", 'yahoo':"399001.SZ",'name':{'chinese':"中国深证成指", 'english':"SZSE COMPONENT INDEX"}},
    {'code':"DJI", 'yahoo':"^DJI",'name':{'chinese':"美国道琼斯工业平均指数", 'english':"Dow Jones Industrial Average"}},
    {'code':"IXIC", 'yahoo':"^IXIC",'name':{'chinese':"美国纳斯达克综合指数", 'english':"NASDAQ Composite"},},
    {'code':"GSPC", 'yahoo':"^GSPC",'name':{'chinese':"美国标准普尔500指数", 'english':"S&P 500"}},
    {'code':"N225", 'yahoo':"^N225",'name':{'chinese':"日本日经225指数", 'english':"NIKKEI 225"}},
    {'code':"TWII", 'yahoo':"^TWII",'name':{'chinese':"台湾台北加权指数", 'english':"TSEC weighted index"}},
    {'code':"HSI", 'yahoo':"^HSI",'name':{'chinese':"香港恒生指数", 'english':"HANG SENG INDEX"}},
    {'code':"FCHI", 'yahoo':"^FCHI",'name':{'chinese':"法国CAC40指数", 'english':"CAC 40"}},
    {'code':"FTSE", 'yahoo':"^FTSE",'name':{'chinese':"英国富时100指数", 'english':"FTSE 100"}},
    {'code':"GDAXI", 'yahoo':"^GDAXI",'name':{'chinese':"德国法兰克福DAX指数", 'english':"DAX"}
    }
]
WorldStockIndexList_SP500 =  WorldStockIndexList[7]

#国内股票数据：指数
def getChinaStockIndexInfo(stockCode, period):
    try:
        exchange = "sz" if (int(stockCode) // 100000 == 3) else "sh"
        #http://hq.sinajs.cn/list=s_sh000001
        dataUrl = "http://hq.sinajs.cn/list=s_" + exchange + stockCode
        # stdout = urllib.request.urlopen(dataUrl)
        # stdoutInfo = stdout.read().decode('gb2312')
        stdoutInfo = requests.get(dataUrl)
        tempData = re.search('''(")(.+)(")''', stdoutInfo).group(2)
        stockInfo = tempData.split(",")
        #stockCode = stockCode,
        stockName   = stockInfo[0]
        stockEnd    = stockInfo[1]  #当前价，15点后为收盘价
        stockZD     = stockInfo[2]  #涨跌
        stockLastEnd= str(float(stockEnd) - float(stockZD)) #开盘价
        stockFD     = stockInfo[3]  #幅度
        stockZS     = stockInfo[4]  #总手
        stockZS_W   = str(int(stockZS) / 100)
        stockJE     = stockInfo[5]  #金额
        stockJE_Y   = str(int(stockJE) / 10000)

        allData = dict()
        data ={
            'code':(str(exchange + stockCode)),
            'name':stockName,
            'now' :stockEnd,
            'open':stockLastEnd,
            'zd':stockZD,
            'zs':stockZS,
            'je':stockJE
            }
        allData['data'] = data
        content = "#" + stockName + "#" + "(" + str(stockCode) + ")" + " 收盘：" \
          + stockEnd + "，\n涨跌：" + stockZD + "，幅度：" + stockFD + "%" \
          + "，总手：" + stockZS_W + "万" + "，金额：" + stockJE_Y + "亿" + "  "

        imgPath = "http://image.sinajs.cn/newchart/" + period + "/n/" + exchange + str(stockCode) + ".gif"
         
        content2 = "#" + stockName + "#" + "(" + str(stockCode) + ")" + "++：" + stockFD + "%" + "，  \n--：" + stockZD \
          + " now：" + stockEnd 

        twitter = {'message': content, 'image': imgPath, 'simple': content2}
        allData['msg'] = twitter
    except Exception as e:
        #print("get indexInfo")
        print(">>>>>> Exception: " + str(e))
    else:
        return allData
    finally:
        None

def drawRand(value, total):
    dd= str(' '+'-'*int(value*total))
    return dd

#国内股票数据：个股
def getChinaStockIndividualInfo(stockCode, period):
    try:
        exchange = "sh" if (int(stockCode) // 100000 == 6) else "sz"
        dataUrl = "http://hq.sinajs.cn/list=" + exchange + stockCode
        # stdout = urllib.request.urlopen(dataUrl)
        # stdoutInfo = stdout.read().decode('gb2312')
        stdoutInfo = requests.get(dataUrl)
        tempData = re.search('''(")(.+)(")''', stdoutInfo).group(2)
        stockInfo = tempData.split(",")
        #stockCode = stockCode,
        stockName   = stockInfo[0]  #名称
        stockStart  = stockInfo[1]  #开盘
        stockLastEnd= stockInfo[2]  #昨收盘
        stockCur    = stockInfo[3]  #当前
        stockMax    = stockInfo[4]  #最高
        stockMin    = stockInfo[5]  #最低
        stockUp     = round(float(stockCur) - float(stockLastEnd), 2)
        stockRange  = round(float(stockUp) / float(stockLastEnd), 4) * 100
        stockVolume = round(float(stockInfo[8]) / (100 * 10000), 2)
        stockMoney  = round(float(stockInfo[9]) / (100000000), 2)
        stockTime   = stockInfo[31]

        alldata = dict()
        data = {
            'code':str(exchange + stockCode),
            'name':stockName,
            'open':stockStart,
            'last':stockLastEnd,
            'now':stockCur,
            'high':stockMax,
            'low':stockMin,
            'up':stockUp,
            'range':stockRange,
            'volume':stockVolume,
            'money':stockMoney,
            'time':stockTime
            }
        alldata['data'] = data
        content = "#" + stockName + "#(" + stockCode + ")" + " 最新:" + stockCur \
        + ",    开盘:" + stockStart + ",最高:" + stockMax + ",最低:" + stockMin \
        + ",\n幅度:" + str(stockRange) + "%" + "   涨跌:" + str(stockUp) \
        + ",总手:" + str(stockVolume) + "万" + ",金额:" + str(stockMoney) \
        + "亿" + ",更新时间:" + stockTime + "  "

        imgUrl = "http://image.sinajs.cn/newchart/" + period + "/n/" + exchange + str(stockCode) + ".gif"

        content2 =  "#" + stockName + "#(" + stockCode + ")" + "  now: " + stockCur + " ,  high:" + stockMax + "  , low:" + stockMin\
        + ",\n" + " "*8 + "++:  " + (str(stockRange))[0:6] + "%" + "    --:  " + str(stockUp) \
        + "  ,time:" + stockTime + " \n" +" "*20 + "Volume :" +str(stockVolume)

        twitter = {'message': content, 'image': imgUrl, 'simple': content2}
        alldata['msg'] = twitter
    except Exception as e:
        #print("get signal")
        print(">>>>>> Exception: " + str(e))
    else:
        return alldata
    finally:
        None

#全球股票指数
def getWorldStockIndexInfo(stockDict):
    try:
        #http://download.finance.yahoo.com/d/quotes.csv?s=^IXIC&f=sl1c1p2l
        yahooCode = stockDict['yahoo']
        dataUrl = "http://download.finance.yahoo.com/d/quotes.csv?s=" + yahooCode + "&f=sl1c1p2l"

        stdout = urllib.request.urlopen(dataUrl)
        stdoutInfo = stdout.read().decode('gb2312')
        tempData = stdoutInfo.replace('"', '')
        stockInfo = tempData.split(",")
        stockNameCn = stockDict['name']['chinese']
        stockNameEn = stockDict['name']['english']
        stockCode   = stockDict['code']
        stockEnd    = stockInfo[1]  #当前价，5点后为收盘价
        stockZD     = stockInfo[2]  #涨跌
        stockLastEnd= str(float(stockEnd) - float(stockZD)) #开盘价
        stockFD     = stockInfo[3]  #幅度
        percent     = float(stockFD.replace("%", ""))
        matchResult = re.search("([\w?\s?:]*)(\-)", stockInfo[4])  #日期和最新值
        stockDate   = matchResult.group(1)

        content = "#" + stockNameCn + "# " + stockNameEn + "(" + stockCode + ")" \
          + " 当前：" + stockEnd + ", 涨跌：" + stockZD + ", 幅度：" + stockFD \
          + ", 最后交易时间：" + stockDate

        twitter = content

    except Exception as err:
        print(">>>>>> Exception: " + yahooCode + " " + str(err))
    else:
        return twitter
    finally:
        None

def test_china_index_data():
    if ChinaStockIndexList == None:
        return None
    data = dict()
    for stockCode in ChinaStockIndexList:
        twitter = getChinaStockIndexInfo(stockCode, period_daily)
        if twitter ==None:
            continue
        print(twitter['msg']['simple'])
        print("********************")


def test_china_individual_data():
    for stockCode in ChinaStockIndividualList:
        twitter = getChinaStockIndividualInfo(stockCode, period_min)
        if twitter ==None:
            continue       
        print(twitter['msg']['simple'])

def test_global_index_data():
    for stockDict in WorldStockIndexList:
        print(getWorldStockIndexInfo(stockDict))
        if twitter ==None:
            return None        


def ddmain():
    "main function"
    #print(base64.b64decode(b'Q29weXJpZ2h0IChjKSAyMDEyIERvdWN1YmUgSW5jLiBBbGwgcmlnaHRzIHJlc2VydmVkLg==').decode())
    totalTime =10000
    while totalTime > 0:
        if (totalTime % 2)== 0:
            test_china_index_data()
            print("==================")
        test_china_individual_data()
        print(totalTime)
        totalTime = totalTime -1
        time.sleep(8)
    #test_global_index_data()


###############################################################
def cal_vga_5_10(msg, _code, _name):
    '''计算 5日均线向上突破10日 买入
           5日均线向下突破10日 卖出
    '''
    if msg == None:
        return None
    money = 200000
    pri = money
    kk = sorted(msg.keys())

    staus = 0
    cun = 0
    freq = 0
    for which in kk[0:]:
        if msg[which]['avg_5'] > (msg[which]['avg_10'])*1 :
            if staus == 0:
                cun = int(money/(100*(1.01*msg[which]['open'])))*100
                if cun < 1 :
                    dd ={
                        'code':_code,
                        'name':_name,
                        'h5_10':((money-pri)/pri),
                        'money':pri,
                        'isout':-1,
                        'freq':freq}
                    return dd
                money = money - cun*(1.01*msg[which]['open'])
                freq += 1
                staus = 1
        elif msg[which]['avg_5'] < (msg[which]['avg_10'])*1.01 :
            if staus == 1:
                money = money + cun*msg[which]['open']
                staus = 0
                freq += 1
                cun = 0
    money = money + cun*msg[kk[-1]]['open']
    dd ={
        'code':_code,
        'name':_name,
        'h5_10':((money-pri)/pri),
        'money':pri,
        'isout':1,
        'freq':freq}
    return dd

###############################################################
def cal_vga_5_10_index(msg, msg2, _code, _name):
    '''计算 在指标数据中 5日均线在10日均线上方
           5日均线向上突破10日 买入
           5日均线向下突破10日 卖出
    '''
    if msg == None:
        return None
    money = 200000
    pri = money
    kk = sorted(msg.keys())

    staus = 0
    cun = 0
    freq = 0
    for which in kk[0:]:
        if (msg[which]['avg_5'] > (msg[which]['avg_10'])*1) and (msg2[which]['avg_5'] > (msg2[which]['avg_10'])*1) and (msg2[which]['avg_10'] > (msg2[which]['avg_24'])*1) :
            if staus == 0:
                cun = int(money/(100*(1.01*msg[which]['open'])))*100
                if cun < 1 :
                    dd ={
                        'code':_code,
                        'name':_name,
                        'h5_10':((money-pri)/pri),
                        'money':pri,
                        'isout':-1,
                        'freq':freq}
                    return dd
                money = money - cun*(1.01*msg[which]['open'])
                freq += 1
                staus = 1
        elif msg[which]['avg_5'] < (msg[which]['avg_10'])*1.01 :
            if staus == 1:
                money = money + cun*msg[which]['open']
                staus = 0
                freq += 1
                cun = 0
    money = money + cun*msg[kk[-1]]['open']
    dd ={
        'code':_code,
        'name':_name,
        'h5_10':((money-pri)/pri),
        'money':pri,
        'isout':1,
        'freq':freq}
    return dd


if __name__ == '__main__':
    pprint.pprint(getAllStockFromTDXandDoIt(20000101, 20151001))
    #pprint.pprint(jj)
    #ddmain()

