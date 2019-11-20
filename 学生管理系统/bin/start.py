#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/8/27 0025 21:21
# @Author : Zhaozhen
# @File : start.py
# @Software: PyCharm

import os
import sys
# 项目路径
base_path = os.path.dirname(os.path.dirname(__file__))
# 添加到sys.path里
sys.path.append(base_path)
from core.main import *

if __name__ == '__main__':
    Main()