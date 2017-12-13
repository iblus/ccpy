# encoding: UTF-8

'''
本文件仅用于存放对于事件类型常量的定义。

由于python中不存在真正的常量概念，因此选择使用全大写的变量名来代替常量。
这里设计的命名规则以EVENT_前缀开头。

常量的内容通常选择一个能够代表真实意义的字符串（便于理解）。

建议将所有的常量定义放在该文件中，便于检查是否存在重复的现象。
'''
 
# 系统相关
EVENT_TIMER = 'eTimer'                  # 计时器事件，每隔1秒发送一次
EVENT_LOG = 'eLog'                      # 日志事件，全局通用

# UI底部状态栏更新
EVENT_UPDATE_STATUS_BAR = 'eUpdateStatusBar'

# 行情相关
EVENT_INDEX_TICK = 'eIndexTick'                 # 大盘指数TICK行情事件
EVENT_GET_SELF_INDEX_TICK = 'eGetSelfIndexTick' # 计算获取自定义指数的事件
EVENT_SELF_INDEX_TICK = 'eSelfIndexTick'        # 自定义指数TICK行情事件
EVENT_SELF_STOCK_TICK = 'eSelfStockTick'        # 自选股TICK行情事件

# 自选股列表的添加与删除
EVENT_SELF_STOCK_ADD = 'eSelfStockListAdd'          #自选股列表添加
EVENT_SELF_STOCK_REMOVE = 'eSelfStockListRemove'    #自选股列表删除

EVENT_TRADE = 'eTrade.'                 # 成交回报事件
EVENT_ORDER = 'eOrder.'                 # 报单回报事件
EVENT_POSITION = 'ePosition.'           # 持仓回报事件
EVENT_ACCOUNT = 'eAccount.'             # 账户回报事件
EVENT_CONTRACT = 'eContract.'           # 合约基础信息回报事件
EVENT_ERROR = 'eError.'                 # 错误回报事件

#----------------------------------------------------------------------
def test():
    """检查是否存在内容重复的常量定义"""
    check_dict = {}
    
    global_dict = globals()    
    
    for key, value in global_dict.items():
        if '__' not in key:                       # 不检查python内置对象
            if value in check_dict:
                check_dict[value].append(key)
            else:
                check_dict[value] = [key]
            
    for key, value in check_dict.items():
        if len(value)>1:
            print(u'存在重复的常量定义:' + str(key))
            for name in value:
                print(name)
            print('')
        
    print(u'测试完毕')
    

# 直接运行脚本可以进行测试
if __name__ == '__main__':
    test()