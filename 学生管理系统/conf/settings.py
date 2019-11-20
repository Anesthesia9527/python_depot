#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/8/27 0025 21:21
# @Author : Zhaozhen
# @File : settings.py
# @Software: PyCharm

import os

# 获取当前项目目录的绝对路径
base = os.path.dirname(os.path.dirname(__file__))
# 获取db目录的绝对路径
db = os.path.join(base,'db')
# 获取log目录的绝对路径
log = os.path.join(base,'log')
# 获取student_info文件的绝对路径
student_info = os.path.join(db,'student_info')
# 获取course_info文件的绝对路径
course_info = os.path.join(db,'course_info')
# 获取user_info文件的绝对路径
user_info = os.path.join(db,'user_info')
# 获取logs.log文件的绝对路径
log_path = os.path.join(log,'logs.log')
