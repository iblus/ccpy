# encoding: UTF-8

"""
通过VT_setting.json加载全局配置
"""

import os
import traceback
import json
from ccFunction import getJsonPath


settingFileName = "VT_setting.json"
settingFilePath = getJsonPath(settingFileName, __file__)

globalSetting = {}      # 全局配置字典

# try:
#     f = open(settingFilePath)
#     globalSetting = json.load(f)
# except:
#     traceback.print_exc()
    
