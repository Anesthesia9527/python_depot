#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/13 0013 23:16
# @Author : Zhaozhen
# @File : settings.py
# @Software: PyCharm

import os
import sys

# 获取当前工作路径
BASE_PATH = os.path.dirname(os.path.dirname(__file__))
# 获取db路径
DB = os.path.abspath(os.path.join(BASE_PATH,'db'))
