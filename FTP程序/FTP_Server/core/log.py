#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/19 0019 17:53
# @Author : Zhaozhen
# @File : log.py.py
# @Software: PyCharm

# 导入要用的模块
import logging
from conf.settings import *


# 创建日志格式
log_file = logging.FileHandler(filename=LOG,encoding='utf-8')
logging.basicConfig(level=logging.INFO,
                    handlers=[log_file],
                    datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)s - %(name)s[%(lineno)d] - %(levelname)s - %(module)s:  %(message)s')