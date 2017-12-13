# encoding: UTF-8

import json
import csv
import os
import platform
from collections import OrderedDict

from eventEngine import *
from eventType import *
from ccFunction import *

import ccText

from uiQt import QtGui, QtWidgets, QtCore, BASIC_FONT, Qt

COLOR_RED = QtGui.QColor('red')
COLOR_GREEN = QtGui.QColor('green')


########################################################################
class BasicCell(QtWidgets.QTableWidgetItem):
    """基础的单元格"""

    #----------------------------------------------------------------------
    def __init__(self, text=None, mainEngine=None):
        """Constructor"""
        super(BasicCell, self).__init__()
        self.data = None
        if text:
            self.setContent(text)
    
    #----------------------------------------------------------------------
    def setContent(self, text):
        """设置内容"""

        # 设置单元格文字右对齐
        self.setTextAlignment(Qt.AlignLeft)

        if text == '0' or text == '0.0':
            self.setText('')
        else:
            self.setText(text)


########################################################################
class NumCell(QtWidgets.QTableWidgetItem):
    """用来显示数字的单元格"""

    #----------------------------------------------------------------------
    def __init__(self, text=None, mainEngine=None):
        """Constructor"""
        super(NumCell, self).__init__()
        self.data = None
        if text:
            self.setContent(text)
    
    #----------------------------------------------------------------------
    def setContent(self, text):
        """设置内容"""
        # 考虑到NumCell主要用来显示OrderID和TradeID之类的整数字段，
        # 这里的数据转化方式使用int类型。但是由于部分交易接口的委托
        # 号和成交号可能不是纯数字的形式，因此补充了一个try...except
        try:
            num = int(text)
            self.setData(QtCore.Qt.DisplayRole, num)
        except ValueError:
            self.setText(text)


########################################################################
class PerNumCell(QtWidgets.QTableWidgetItem):
    """用来显示百分比的单元格"""

    # ----------------------------------------------------------------------
    def __init__(self, text=None, mainEngine=None):
        """Constructor"""
        super(PerNumCell, self).__init__()
        self.data = None
        if text:
            self.setContent(text)

    # ----------------------------------------------------------------------
    def setContent(self, text):
        """设置内容"""

        # 设置单元格文字右对齐
        self.setTextAlignment(Qt.AlignRight)

        # PerNumCell主要用来显示保留两位小数的百分比
        #
        # 号和成交号可能不是纯数字的形式，因此补充了一个try...except
        try:
            num = float(text)
            if num >=0:
                self.setForeground(COLOR_RED)
            else:
                self.setForeground(COLOR_GREEN)

            num = '%.2f%%'%((float(text))*100)
            self.setText(num)
        except ValueError as err:
            print(err)
            self.setText('err')


########################################################################
class PnlCell(QtWidgets.QTableWidgetItem):
    """显示盈亏的单元格"""

    #----------------------------------------------------------------------
    def __init__(self, text=None, mainEngine=None):
        """Constructor"""
        super(PnlCell, self).__init__()
        self.data = None
        self.color = ''
        if text:
            self.setContent(text)
    
    #----------------------------------------------------------------------
    def setContent(self, text):
        """设置内容"""
        self.setText(text)

        try:
            value = float(text)
            if value >= 0 and self.color != 'red':
                self.color = 'red'
                self.setForeground(COLOR_RED)
            elif value < 0 and self.color != 'green':
                self.color = 'green'
                self.setForeground(COLOR_GREEN)
        except Exception as err:
            print(err)
            pass


########################################################################
class BasicMonitor(QtWidgets.QTableWidget):
    """
    基础监控
    
    headerDict中的值对应的字典格式如下
    {'chinese': u'中文名', 'cellType': BasicCell}
    
    """
    signal = QtCore.pyqtSignal(type(Event()))

    #----------------------------------------------------------------------
    def __init__(self, mainEngine=None, eventEngine=None, parent=None):
        """Constructor"""
        super(BasicMonitor, self).__init__(parent)
        
        self.mainEngine = mainEngine
        self.eventEngine = eventEngine
        
        # 保存表头标签用
        self.headerDict = OrderedDict()  # 有序字典，key是英文名，value是对应的配置字典
        self.headerList = []             # 对应self.headerDict.keys()
        
        # 保存相关数据用
        self.dataDict = {}  # 字典，key是字段对应的数据，value是保存相关单元格的字典
        self.dataKey = ''   # 字典键对应的数据字段
        
        # 监控的事件类型
        self.eventType = ''
        
        # 列宽调整状态（只在第一次更新数据时调整一次列宽）
        self.columnResized = False
        
        # 字体
        self.font = None
        
        # 保存数据对象到单元格
        self.saveData = False
        
        # 默认不允许根据表头进行排序，需要的组件可以开启
        self.sorting = False

        # 默认每次新添加一行数据到最后一行
        self.insertFirstRow = False
        
    #----------------------------------------------------------------------
    def setHeaderDict(self, headerDict):
        """设置表头有序字典"""
        self.headerDict = headerDict
        self.headerList = headerDict.keys()
        
    #----------------------------------------------------------------------
    def setDataKey(self, dataKey):
        """设置数据字典的键"""
        self.dataKey = dataKey
        
    #----------------------------------------------------------------------
    def setEventType(self, eventType):
        """设置监控的事件类型"""
        self.eventType = eventType
        
    #----------------------------------------------------------------------
    def setFont(self, font):
        """设置字体"""
        self.font = font
    
    #----------------------------------------------------------------------
    def setSaveData(self, saveData):
        """设置是否要保存数据到单元格"""
        self.saveData = saveData
        
    #----------------------------------------------------------------------
    def initTable(self):
        """初始化表格"""
        # 设置表格的列数
        col = len(self.headerDict)
        self.setColumnCount(col)
        
        # 设置列表头
        labels = [d['chinese'] for d in self.headerDict.values()]
        self.setHorizontalHeaderLabels(labels)
        # 使行列头自适应宽度，最后一列将会填充空白部分
        self.horizontalHeader().setStretchLastSection(True)
        # 使行列头自适应宽度，所有列平均分来填充空白部分
        self.horizontalHeader().setResizeContentsPrecision(QtWidgets.QHeaderView.Stretch)
        
        # 关闭左边的垂直表头
        self.verticalHeader().setVisible(False)
        # 使行自适应高度，假如行很多的话，行的高度不会一直减小，当达到一定值时会自动生成一个QScrollBar
        # self.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        
        # 设为不可编辑
        self.setEditTriggers(self.NoEditTriggers)
        
        # 设为行交替颜色
        self.setAlternatingRowColors(True)

        # 隐藏边框
        self.setShowGrid(False)
        # 隐藏外边框
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        
        # 设置允许排序
        self.setSortingEnabled(self.sorting)

        # 设置按行选中
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        # 设置只能选择一行，不能选择多行
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)


    #----------------------------------------------------------------------
    def registerEvent(self):
        """注册GUI更新相关的事件监听"""
        self.signal.connect(self.updateEvent)
        self.eventEngine.register(self.eventType, self.signal.emit)
        
    #----------------------------------------------------------------------
    def updateEvent(self, event):
        """收到事件更新"""
        data = event.dict_['data']
        self.updateData(data)
    
    #----------------------------------------------------------------------
    def updateData(self, data):
        """将数据更新到表格中"""

        # 如果允许了排序功能，则插入数据前必须关闭，否则插入新的数据会变乱
        if self.sorting:
            self.setSortingEnabled(False)
        if self.insertFirstRow:
            nowRow = 0
        else:
            nowRow = self.rowCount()
        
        # 如果设置了dataKey，则采用存量更新模式
        if self.dataKey:
            key = data.__getattribute__(self.dataKey)
            # 如果键在数据字典中不存在，则先插入新的一行，并创建对应单元格
            if key not in self.dataDict:
                self.insertRow(nowRow)
                d = {}
                for n, header in enumerate(self.headerList):                  
                    content = safeUnicode(data.__getattribute__(header))
                    cellType = self.headerDict[header]['cellType']
                    cell = cellType(content, self.mainEngine)
                    
                    if self.font:
                        cell.setFont(self.font)  # 如果设置了特殊字体，则进行单元格设置
                    
                    if self.saveData:            # 如果设置了保存数据对象，则进行对象保存
                        cell.data = data

                    self.setItem(nowRow, n, cell)
                    d[header] = cell
                self.dataDict[key] = d
            # 否则如果已经存在，则直接更新相关单元格
            else:
                d = self.dataDict[key]
                for header in self.headerList:
                    content = safeUnicode(data.__getattribute__(header))
                    cell = d[header]
                    cell.setContent(content)
                    
                    if self.saveData:            # 如果设置了保存数据对象，则进行对象保存
                        cell.data = data                    
        # 否则采用增量更新模式
        else:
            self.insertRow(nowRow)
            for n, header in enumerate(self.headerList):
                content = safeUnicode(data.__getattribute__(header))
                cellType = self.headerDict[header]['cellType']
                cell = cellType(content, self.mainEngine)
                
                if self.font:
                    cell.setFont(self.font)

                if self.saveData:
                    cell.data = data                

                self.setItem(nowRow, n, cell)
                
        # 调整列宽
        if self.columnResized:
            self.resizeColumnsToContents()
            self.resizeRowsToContents()
            # self.horizontalHeader().resizeSection(0,140)
        
        # 重新打开排序
        if self.sorting:
            self.setSortingEnabled(True)
    
    #----------------------------------------------------------------------
    def resizeColumns(self):
        """调整各列的大小"""
        self.horizontalHeader().resizeSections(QtWidgets.QHeaderView.ResizeToContents)    
        
    #----------------------------------------------------------------------
    def setSorting(self, sorting):
        """设置是否允许根据表头排序"""
        self.sorting = sorting


########################################################################

class IndexMonitor(BasicMonitor):
    """大盘指数监控组件"""

    # ----------------------------------------------------------------------
    def __init__(self, mainEngine, eventEngine, parent=None):
        """Constructor"""
        super(IndexMonitor, self).__init__(mainEngine, eventEngine, parent)

        # 设置表头有序字典
        d = OrderedDict()
        d['symbol'] = {'chinese': ccText.STOCK_SYMBOL, 'cellType': BasicCell}
        d['name'] = {'chinese': ccText.STOCK_NAME, 'cellType': BasicCell}
        d['lastPrice'] = {'chinese': ccText.LAST_PRICE, 'cellType': BasicCell}

        d['chg'] = {'chinese': ccText.CHANGEPER_PRICE, 'cellType': PnlCell}
        d['time'] = {'chinese': ccText.TIME, 'cellType': BasicCell}

        self.setHeaderDict(d)

        # 设置数据键
        self.setDataKey('symbol')

        # 设置监控事件类型
        self.setEventType(EVENT_INDEX_TICK)

        # 设置字体
        self.setFont(BASIC_FONT)

        # 设置允许排序
        self.setSorting(True)

        # 初始化表格
        self.initTable()

        # 注册事件监听
        self.registerEvent()

########################################################################

class SelfStockMonitor(BasicMonitor):
    """自选股监控组件"""

    # ----------------------------------------------------------------------
    def __init__(self, mainEngine, eventEngine, parent=None):
        """Constructor"""
        super(SelfStockMonitor, self).__init__(mainEngine, eventEngine, parent)

        # 设置表头有序字典
        d = OrderedDict()
        d['symbol'] = {'chinese': ccText.STOCK_SYMBOL, 'cellType': BasicCell}
        d['name'] = {'chinese': ccText.STOCK_NAME, 'cellType': BasicCell}
        d['lastPrice'] = {'chinese': ccText.LAST_PRICE, 'cellType': BasicCell}
        d['changePerPrice'] = {'chinese': ccText.CHANGEPER_PRICE, 'cellType': PerNumCell}
        d['time'] = {'chinese': ccText.TIME, 'cellType': BasicCell}

        self.setHeaderDict(d)

        # 设置数据键
        self.setDataKey('symbol')

        # 设置监控事件类型
        self.setEventType(EVENT_SELF_STOCK_TICK)

        # 设置字体
        self.setFont(BASIC_FONT)

        # 初始化表格
        self.initTable()

        # ----------------------------
        # 去除鼠标点中时的虚框
        self.setFocusPolicy(Qt.NoFocus)
        # 垂直表头不显示
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)
        # 设置表格不可编辑
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # 设置水平滚动条不显示
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 垂直滚动条按项移动
        self.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 去掉自动滚动
        self.setAutoScroll(False)

        # 设置允许排序
        self.setSorting(False)

        # 注册事件监听
        self.registerEvent()

########################################################################

class SelfIndexMonitor(BasicMonitor):
    """自定义指数监控组件"""

    # ----------------------------------------------------------------------
    def __init__(self, mainEngine, eventEngine, parent=None):
        """Constructor"""
        super(SelfIndexMonitor, self).__init__(mainEngine, eventEngine, parent)

        # 设置表头有序字典
        d = OrderedDict()
        # d['symbol'] = {'chinese': ccText.STOCK_SYMBOL, 'cellType': BasicCell}
        d['name'] = {'chinese': ccText.STOCK_NAME, 'cellType': BasicCell}
        d['lastPrice'] = {'chinese': ccText.LAST_PRICE, 'cellType': BasicCell}
        d['tip']  = {'chinese': ccText.MSG, 'cellType': BasicCell}
        # d['time'] = {'chinese': ccText.TIME, 'cellType': BasicCell}

        self.setHeaderDict(d)

        # 设置数据键
        self.setDataKey('symbol')

        # 设置监控事件类型
        self.setEventType(EVENT_SELF_INDEX_TICK)

        # 设置字体
        self.setFont(BASIC_FONT)

        # 初始化表格
        self.initTable()

        # ----------------------------
        # 去除鼠标点中时的虚框
        self.setFocusPolicy(Qt.NoFocus)
        # 垂直表头不显示
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)
        # 设置表格不可编辑
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # 设置水平滚动条不显示
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 垂直滚动条按项移动
        self.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 去掉自动滚动
        self.setAutoScroll(False)

        # 设置允许排序
        self.setSorting(False)

        # 注册事件监听
        self.registerEvent()


########################################################################
class LogMonitor(BasicMonitor):
    """日志监控"""

    #----------------------------------------------------------------------
    def __init__(self, mainEngine, eventEngine, parent=None):
        """Constructor"""
        super(LogMonitor, self).__init__(mainEngine, eventEngine, parent)
        
        d = OrderedDict()        
        d['logTime'] = {'chinese':ccText.TIME, 'cellType':BasicCell}
        d['logContent'] = {'chinese':ccText.CONTENT, 'cellType':BasicCell}
        d['gatewayName'] = {'chinese':ccText.GATEWAY, 'cellType':BasicCell}
        self.setHeaderDict(d)
        
        self.setEventType(EVENT_LOG)
        self.setFont(BASIC_FONT)        
        self.initTable()
        self.registerEvent()


########################################################################
class ErrorMonitor(BasicMonitor):
    """错误监控"""

    #----------------------------------------------------------------------
    def __init__(self, mainEngine, eventEngine, parent=None):
        """Constructor"""
        super(ErrorMonitor, self).__init__(mainEngine, eventEngine, parent)
        
        d = OrderedDict()       
        d['errorTime']  = {'chinese':ccText.TIME, 'cellType':BasicCell}
        d['errorID'] = {'chinese':ccText.ERROR_CODE, 'cellType':BasicCell}
        d['errorMsg'] = {'chinese':ccText.ERROR_MESSAGE, 'cellType':BasicCell}
        d['gatewayName'] = {'chinese':ccText.GATEWAY, 'cellType':BasicCell}
        self.setHeaderDict(d)
        
        self.setEventType(EVENT_ERROR)
        self.setFont(BASIC_FONT)
        self.initTable()
        self.registerEvent()

