#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/14 0014 22:40
# @Author : Zhaozhen
# @File : progress_bar.py
# @Software: PyCharm

import sys
import time
# from core import log

def humanbytes(B):
    B = float(B)
    KB = float(1024)
    MB = float(KB ** 2)
    GB = float(KB ** 3)
    TB = float(KB ** 4)
    if B < KB:
        return '{0} {1}'.format(B, 'Bytes' if 0 == B > 1 else 'Byte')
    elif KB <= B < MB:
        return '{0:.2f} KB'.format(B / KB)
    elif MB <= B < GB:
        return '{0:.2f} MB'.format(B / MB)
    elif GB <= B < TB:
        return '{0:.2f} GB'.format(B / GB)
    elif TB <= B:
        return '{0:.2f} TB'.format(B / TB)

def progres(num,Sum,bytes):
    """
    显示上传进度条
    num：已上传大小
    Sum：文件总大小
    #l：定义进度条大小
    """
    bar_length = 50  # 定义进度条大小
    percent = float(num) / float(Sum)
    hashes = '=' * int(percent * bar_length)  # 定义进度显示的数量长度百分比
    spaces = ' ' * (bar_length - len(hashes))  # 定义空格的数量=总长度-显示长度

    sys.stdout.write(
        "\r%s: [%s] %d%%  %s/%s" % (bytes,hashes + spaces, percent * 100, humanbytes(num), humanbytes(Sum)))  # 输出显示进度条
    sys.stdout.flush()  # 强制刷新到屏幕