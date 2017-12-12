#-*- coding:utf-8 -*-
import os
import sys
import pprint
import datetime

import csv
import xlrd
import xlwt
import xlsxwriter
import openpyxl

def readCSV(_file):
    try:
        if os.path.exists(_file)==False:
            print('the file %s is not exit!!!'%(_file))
            return -1
        with open(_file, newline='') as f:
            reader = csv.reader(f, delimiter=',', quotechar='|')
            for i in reader:
                print(i)
    except Exception as err:
        print(">>>>>> Exception: " + str(err))
        return -1
    else:
        return 0
    finally:
        None


def writeCSV(_file):
    try:
        with open(_file, 'w') as f:
            spamwriter = csv.writer(f, dialect='excel', delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            #spamwriter = csv.writer(f, dialect='excel')
            data_list = ['a', '1', 2]
            spamwriter.writerow(['a', '1', 3])
            spamwriter.writerow(data_list)
    except Exception as err:
        print(">>>>>> Exception: " + str(err))
        return -1
    else:
        return 0
    finally:
        None



def readXL(_file):
    try:
        if os.path.exists(_file) == False:
            print('the file %s is not exit!!!'%(_file))
            return -1
        data = xlrd.open_workbook(_file) 
        #table = data.sheets()[0] #通过索引顺序获取
        table = data.sheet_by_index(0) #通过索引顺序获取
        #table = data.sheet_by_name(u'Sheet1') #通过名称获取
        
        nrows = table.nrows
        ncols = table.ncols
        colnames = table.row_values(0) #第一行的数据, 作为表头
        #colnames = table.col_values(0) # 第一列的数据
        
        list = []
        for rownum in range(1, nrows):
            row = table.row_values(rownum)
            if row:
                app = {}
                for i in range(len(colnames)):
                    app[colnames[i]] = row[i]
                list.append(app)
        return list

    except Exception as err:
        print(">>>>>> Exception: " + str(err))
        return None
    finally:
        None

def writeXLS(_file):
    try:
        #新建excel文件
        wbk = xlwt.Workbook()
        wbk.encoding = 'utf-8'
        #新建一个sheet
        sheet = wbk.add_sheet('sheet 1', cell_overwrite_ok=True)
        #配置数据的字体风格
        style = xlwt.easyxf(
            'font: name Arial, bold True, underline True, italic True;'
            'pattern: pattern solid, fore_colour green;'
            )
        #插入位图
        #sheet.insert_bitmap('0001.bmp',5,5)
        #插入公式
        sheet.write(3,3,xlwt.Formula('SUM(A1,A2)'))
        #写入数据(行,列,数据)
        #sheet.write(0,1, 'test textfcf', style)
        sheet.write(0,0, 3)
        sheet.write(1,0, 5)
        
        

        #保存文件
        wbk.save(_file)
        return 0

    except Exception as err:
        print(">>>>>> Exception: " + str(err))
        return -1
    finally:
        None

def writeXLSX(_file):
    try:
        wbk = xlsxwriter.Workbook(_file)
        sheet = wbk.add_worksheet('sheet 1')

        sheet.write('A1', 'Hello world')
        sheet.write(0,1,9)
        sheet.write(0,2,8)
        sheet.write(1,1,'=SUM(B1:C1)')
        sheet.write_formula(1,1,'=SUM(B1:C1)')

        wbk.close()
        return 0
    except Exception as err:
        print(">>>>>> Exception: " + str(err))
        return -1
    finally:
        None

if __name__ == '__main__':
    writeXLSX('fdf.xlsx')
