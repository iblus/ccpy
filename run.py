# encoding: UTF-8

# 重载sys模块，设置默认字符串编码方式为utf8
import sys

# 判断操作系统
import platform
system = platform.system()

# vn.trader模块
from eventEngine import EventEngine2
from ccEngine import MainEngine
from uiQt import createQApp, QtCore
from uiMainWindow import MainWindow

import signal,sys

def exit(signum, frame):
    print('You choose to stop me?')
    # sys.exit(0)


#----------------------------------------------------------------------
def main():
    signal.signal(signal.SIGINT, exit)
    signal.signal(signal.SIGTERM, exit)
    """主程序入口"""
    # 创建Qt应用对象
    qApp = createQApp()
    
    # 创建事件引擎
    ee = EventEngine2()
    
    # 创建主引擎
    me = MainEngine(ee)


    # 创建主窗口
    mw = MainWindow(me, ee)
    mw.showMaximized()

    
    # 在主线程中启动Qt事件循环
    sys.exit(qApp.exec_())


if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        print(err)
