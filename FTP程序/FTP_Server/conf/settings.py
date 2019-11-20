#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/11 0011 22:33
# @Author : Zhaozhen
# @File : settings.py
# @Software: PyCharm

import os

# 获取当前工作路径
BASE_PATH = os.path.dirname(os.path.dirname(__file__))
# 获取db路径
DB = os.path.abspath(os.path.join(BASE_PATH,'db'))
# 获取用户信息文件路径
USER_INFO = os.path.join(DB,'user_info')
# 获取log路径
LOG = os.path.join(BASE_PATH,'log','logs.log')