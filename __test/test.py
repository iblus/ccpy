import sys,os
import logging

def get_cur_info(msg):
    print(sys._getframe().f_back.f_code.co_name)
    print(sys._getframe().f_back.f_lineno)
    print(msg)

def printErr(msg):
    """打印错误信息，添加出错文件名和所在行号"""

    # 创建logger
    logger = logging.getLogger()
    #定义输出格式
    formatter = logging.Formatter('%(filename)s:%(funcName)s:%(lineno)d --> %(message)s')

    # 将log信息打印到文件
    # fh = logging.FileHandler('test.log')
    # fh.setFormatter(formatter)
    # logger.addHandler(fh)

    # 将log信息打印到控制台
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.error(msg)

if __name__ == '__main__':
    printErr('lklfffffff')