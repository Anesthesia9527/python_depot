#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/9 0009 15:251
# @Author : Zhaozhen
# @File : client_start.py
# @Software: PyCharm

import os
import sys
import socket

# 获取工作路径
BASE_PATH = os.path.dirname(os.path.dirname(__file__))
# 添加本地全局
sys.path.append(BASE_PATH)
# 导入main主函数模块
from core.main import main

if __name__ == '__main__':
    main()
