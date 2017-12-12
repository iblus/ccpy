#!/usr/local/bin/python3
#coding=utf-8
#source http://www.cnblogs.com/txw1958/

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
    #"601600", #  中国铝业
    #"002415", #  海康威视
    #"600500", #  中化国际
    #"600787", #  中储股份
    #"000063", #  中兴通讯
    #"600839", #  四川长虹
    #"600050", #  中国联通
    #"001696", #  宗申动力
    #"002230", #  科大讯飞
    #"600498", #  烽火通信
    #"000883", #  湖北能源
    #"002594", #比亚迪
    #"600893",
    #"600620", #天宸股份
    #"000100", #  TCL
    #"002184", #海得控制
    #"000829", #天音控股
    #"600642", #申能股份
    #"600594", #益佰制药
    #"002292", #奥飞动漫
    #"601211", #国泰君安
    #"603616", #韩建河山
    
    #"000025", #特力A
    #"603025", #大豪科技
    #"002276", #万马股份
    #"600853", #龙建股份
    #"000503", #海虹控股
    
    #"603085", #天成自控
    #"601313", #江南嘉捷
    #"002312", #三泰控股
    #"002747", #埃斯顿
    #"600868", #梅雁吉祥
    #"002765", #蓝黛传动
    #"600112", #天成控股
    #"002170", #芭田股份
    #"000693", #华泽钴镍
    #"002772", #众兴菌业
    #"600461", #洪城水业
    #"601515", #东风股份
    #"600684", #珠江实业
    #"002024", #苏宁云商
    #"600415", #小商品城
    #"600601", #方正科技
    #"600122", #宏图高科
    #"600458", #时代新材
    #"002378", #章源钨业
    #"300453", #三鑫医疗
    #"002432", #九安医疗
    #"300244", #迪安诊断
    #"002551", #尚荣医疗
    #"300015", #爱尔眼科
    #"300273", #和佳股份
    #"002242", #九阳股份
    #"600133", #东湖高新
    #"000410", #沈阳机床
    #"600676", #交运股份
    #"000988", #华工科技
    

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
        stdout = urllib.request.urlopen(dataUrl)
        stdoutInfo = stdout.read().decode('gb2312')
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
        stdout = urllib.request.urlopen(dataUrl)
        stdoutInfo = stdout.read().decode('gb2312')
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


def test_china_individual_data(stockList=ChinaStockIndividualList):
    if stockList == None:
        return None
    for stockCode in stockList:
        twitter = getChinaStockIndividualInfo(stockCode, period_min)
        if twitter ==None:
            continue       
        print(twitter['msg']['simple'])

def test_global_index_data():
    for stockDict in WorldStockIndexList:
        twitter = getWorldStockIndexInfo(stockDict)
        print(twitter)
        if twitter ==None:
            return None        


def ddmain(totalTime = 10000,sleep = 2):
    "main function"
    #print(base64.b64decode(b'Q29weXJpZ2h0IChjKSAyMDEyIERvdWN1YmUgSW5jLiBBbGwgcmlnaHRzIHJlc2VydmVkLg==').decode())
    while totalTime > 0:
        if (totalTime % 2)== 0:
            os.system('cls')
            test_china_index_data()
            print("==================")
        test_china_individual_data()
        print(totalTime)
        totalTime = totalTime -1
        time.sleep(sleep)
    #test_global_index_data()


if __name__ == '__main__':
    ddmain()
    
