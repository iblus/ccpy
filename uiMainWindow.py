# encoding: UTF-8

import psutil
import traceback
import time
from uiBasicWidget import *
from PyQt5.QtCore import Qt

########################################################################
class MainWindow(QtWidgets.QMainWindow):
    """主窗口"""  

    signalStatusBar = QtCore.pyqtSignal(type(Event()))

    #----------------------------------------------------------------------
    def __init__(self, mainEngine, eventEngine):
        """Constructor"""          
        super(MainWindow, self).__init__()
        
        self.mainEngine = mainEngine
        self.eventEngine = eventEngine
        
        self.widgetDict = {}    # 用来保存子窗口的字典
        
        self.initUi()
        # self.loadWindowSettings('custom')
        
    #----------------------------------------------------------------------
    def initUi(self):
        """初始化界面"""
        self.setWindowTitle('ccMarket')
        self.initCentral()
        self.initStatusBar()

        # self.setWindowFlags(Qt.WindowMaximizeButtonHint)

        self.resize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setSizePolicy(sizePolicy)
        self.setMaximumSize(QtCore.QSize(800, 600))

        screen = QtWidgets.QDesktopWidget().screenGeometry()
        size = self.geometry()
        # self.move(int((screen.width() - size.width())/2), int((screen.height() - size.height())/2))
        self.move(500, 500)

        #----------------------------------------------------------------------
    def initCentral(self):

        """初始化中心区域"""


        self.centralwidget = QtWidgets.QWidget()
        self.gridLayout_0 = QtWidgets.QGridLayout(self.centralwidget)


        # ------------------------------------
        # 用于异动提醒
        groupBox_0 = QtWidgets.QGroupBox()
        groupBox_0.setTitle(u"个股异动")
        gridLayout = QtWidgets.QGridLayout(groupBox_0)
        self.tableWidget_yidong = AStockMarketMonitor(self.mainEngine, self.eventEngine)
        gridLayout.addWidget(self.tableWidget_yidong)

        self.gridLayout_0.addWidget(groupBox_0, 0, 0, 1, 2)

        ##
        self.verticalLayout_0_0 = QtWidgets.QVBoxLayout()
        ##自定义指标控件
        groupBox_1 = QtWidgets.QGroupBox()
        groupBox_1.setTitle(u"大盘赚钱效应")
        gridLayout = QtWidgets.QGridLayout(groupBox_1)

        self.tableWidget_index = SelfIndexMonitor(self.mainEngine, self.eventEngine)
        gridLayout.addWidget(self.tableWidget_index)
        self.verticalLayout_0_0.addWidget(groupBox_1)

        ##自选股行情
        groupBox_2 = QtWidgets.QGroupBox()
        groupBox_2.setTitle(u"自选情况")
        gridLayout = QtWidgets.QGridLayout(groupBox_2)
        self.tableWidget_selfStock = SelfStockMonitor(self.mainEngine,self.eventEngine)
        gridLayout.addWidget(self.tableWidget_selfStock)
        self.verticalLayout_0_0.addWidget(groupBox_2)

        ## 自选输入控件
        gridLayout = QtWidgets.QGridLayout()
        self.lineEdit = QtWidgets.QLineEdit()
        self.radioButton = QtWidgets.QRadioButton()
        self.pushButton = QtWidgets.QPushButton()

        ### 配置输入框索引
        completerStr = self.mainEngine.allStockList['tip']
        if completerStr is None:
            completerStr = ['error']

        completer = QtWidgets.QCompleter(completerStr)
        completer.setCaseSensitivity(False)
        completer.setFilterMode(Qt.MatchContains)
        self.lineEdit.setCompleter(completer)
        self.lineEdit.setFocus()
        self.lineEdit.textEdited.connect(self.onCompleterActivated)
        completer.activated.connect(self.onCompleterActivated)

        gridLayout.addWidget(self.radioButton,0,0,1,1)
        gridLayout.addWidget(self.lineEdit,1,0,1,1)
        gridLayout.addWidget(self.pushButton,1,2,1,1)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)

        gridLayout.setColumnStretch(0,2)
        gridLayout.setColumnStretch(1,3)

        self.verticalLayout_0_0.addLayout(gridLayout)

        self.verticalLayout_0_0.setStretch(0, 3)
        self.verticalLayout_0_0.setStretch(1, 5)
        self.verticalLayout_0_0.setStretch(2, 1)

        self.gridLayout_0.addLayout(self.verticalLayout_0_0, 0, 2, 1, 4)

        #指标绘图控件

        self.mpl_layout = QtWidgets.QGridLayout()

        gridLayout = QtWidgets.QGridLayout()
        gridLayout.setContentsMargins(0, 0, 0, 0)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        gridLayout.addItem(spacerItem, 1, 0, 1, 1)

        gridLayout.addLayout(self.mpl_layout, 0, 0, 1, 1)
        gridLayout.setRowStretch(0, 3)
        gridLayout.setRowStretch(1, 2)

        # --------------------------------------
        # self.gridLayout_0.addLayout(gridLayout, 0, 2, 1, 1)
        # self.gridLayout_0.setColumnStretch(0, 2)
        # self.gridLayout_0.setColumnStretch(1, 3)

        self.setCentralWidget(self.centralwidget)
    
        # 连接组件之间的信号
        # widgetIndexM.itemDoubleClicked.connect(widgetSelfIndexM.closePosition)
        
        # 保存默认设置
        # self.saveWindowSettings('default')

    #----------------------------------------------------------------------
    def initStatusBar(self):
        """初始化状态栏"""
        self.statusLabel = QtWidgets.QLabel()
        self.statusLabel.setAlignment(QtCore.Qt.AlignLeft)
        
        self.statusBar().addPermanentWidget(self.statusLabel)
        # self.statusLabel.setText(time.strftime('%Y-%m-%d %A  %H:%M:%S'))
        
        # self.sbCount = 0
        # self.sbTrigger = 1     # 10秒刷新一次
        self.signalStatusBar.connect(self.updateStatusBar)
        self.eventEngine.register(EVENT_UPDATE_STATUS_BAR, self.signalStatusBar.emit)
        
    #----------------------------------------------------------------------
    def updateStatusBar(self, event):
        """在状态栏更新CPU和内存信息"""
        # self.sbCount += 1
        
        # if self.sbCount == self.sbTrigger:
        #     self.sbCount = 0
            # self.statusLabel.setText(self.getCpuMemory())
            # self.statusLabel.setText(time.strftime('%Y-%m-%d %A  %H:%M:%S'))
        self.statusLabel.setText(event.dict_['data'].name)
    
    #----------------------------------------------------------------------
    def getCpuMemory(self):
        """获取CPU和内存状态信息"""
        cpuPercent = psutil.cpu_percent()
        memoryPercent = psutil.virtual_memory().percent
        return ccText.CPU_MEMORY_INFO.format(cpu=cpuPercent, memory=memoryPercent)

    #------------------------------------
    def onCompleterActivated(self, msg):
        """代码输入框自动匹配"""
        key = self.mainEngine.allStockList
        code = msg[0:6]

        da = key[key.tip.str.find(msg.upper()) != -1]
        if len(da) == 0:
            self.lineEdit.setText('')
            return
        if len(da) != 1:
            return
        if len(da) == 1:
            self.lineEdit.setText(da.iloc[0,3])
            code = da.iloc[0,0]

        print(code)

        event = Event(EVENT_SELF_STOCK_ADD)
        event.dict_['data'] = code
        self.eventEngine.put(event)

        #put event

        
    #----------------------------------------------------------------------
    def test(self):
        """测试按钮用的函数"""
        # 有需要使用手动触发的测试函数可以写在这里
        pass


    #----------------------------------------------------------------------
    def closeEvent(self, event):
        """关闭事件"""
        """
        reply = QtWidgets.QMessageBox.question(self, ccText.EXIT,
                                           ccText.CONFIRM_EXIT, QtWidgets.QMessageBox.Yes |
                                           QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        """
        if True:#reply == QtWidgets.QMessageBox.Yes:
            for widget in self.widgetDict.values():
                widget.close()
            self.saveWindowSettings('custom')
            
            self.mainEngine.exit()
            event.accept()
        else:
            event.ignore()
            
    #----------------------------------------------------------------------
    def createDock(self, widgetClass, widgetName, widgetArea):
        """创建停靠组件"""
        widget = widgetClass(self.mainEngine, self.eventEngine)
        dock = QtWidgets.QDockWidget(widgetName)
        dock.setWidget(widget)
        dock.setObjectName(widgetName)
        dock.setFeatures(dock.DockWidgetFloatable|dock.DockWidgetMovable)
        self.addDockWidget(widgetArea, dock)
        return widget, dock
    
    #----------------------------------------------------------------------
    def saveWindowSettings(self, settingName):
        """保存窗口设置"""
        settings = QtCore.QSettings('vn.trader', settingName)
        settings.setValue('state', self.saveState())
        settings.setValue('geometry', self.saveGeometry())
        
    #----------------------------------------------------------------------
    def loadWindowSettings(self, settingName):
        """载入窗口设置"""
        settings = QtCore.QSettings('vn.trader', settingName)           
        state = settings.value('state')
        geometry = settings.value('geometry')
        
        # 尚未初始化
        if state is None:
            return
        # 老版PyQt
        elif isinstance(state, QtCore.QVariant):
            self.restoreState(state.toByteArray())
            self.restoreGeometry(geometry.toByteArray())
        # 新版PyQt
        elif isinstance(state, QtCore.QByteArray):
            self.restoreState(state)
            self.restoreGeometry(geometry)
        # 异常
        else:
            content = u'载入窗口配置异常，请检查'
            self.mainEngine.writeLog(content)
        
    #----------------------------------------------------------------------
    def restoreWindow(self):
        """还原默认窗口设置（还原停靠组件位置）"""
        self.loadWindowSettings('default')
        self.showMaximized()


########################################################################
class AboutWidget(QtWidgets.QDialog):
    """显示关于信息"""

    #----------------------------------------------------------------------
    def __init__(self, parent=None):
        """Constructor"""
        super(AboutWidget, self).__init__(parent)

        self.initUi()

    #----------------------------------------------------------------------
    def initUi(self):
        """"""
        self.setWindowTitle(ccText.ABOUT + 'VnTrader')

        text = u"""
            Developed by Traders, for Traders.

            License：MIT
            
            """

        label = QtWidgets.QLabel()
        label.setText(text)
        label.setMinimumWidth(500)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(label)

        self.setLayout(vbox)
    