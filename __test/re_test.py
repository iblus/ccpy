
# coding=utf-8
import os,sys
from pprint import pprint
import requests
import re
from lxml import html

import json
import tushare as ts
import pandas as pd

import unittest


def test_re():
    p1 = re.compile(r'abb*?')
    str1 = 'abbc\nabb'
    print(p1.findall(str1))

def get_holder():
    req = requests.get("http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockHolder/stockid/603986/displaytype/10.phtml")
    req.encoding = 'gbk'

    # with open('out/sina.html.txt','w+') as fp:
    #     fp.write(req.text)

    p = re.compile(r'.*HoldStockState.*?>(.*?)<')
    p1 = re.compile(r'.*StockHolderAmount.*?holdstocknum.*?>(.*?)<')
    p2 = re.compile(r'.*StockHolderAmount.*?holdstockproportion.*?>(.*?)<')
    p3 = re.compile(r'.*StockHolderAmount.*?holdstocknum.*?>(.*?)<.*?StockHolderAmount.*?holdstockproportion.*?>(.*?)<')

    ret = p.findall(req.text)
    # ret = p1.findall(req.text)
    # ret = p3.findall(req.text)
    pprint(ret)
    ip_addr = re.search('(\d{3}\.){1,3}\d{1,3}\.\d{1,3}', os.popen('ipconfig').read())

def test():
    req = requests.get("http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockHolder/stockid/603986/displaytype/10.phtml")
    req.encoding = 'gbk'

    get_holder()

if __name__ =="__main__":
    test()
