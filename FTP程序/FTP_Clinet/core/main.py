#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/12 0012 17:19
# @Author : Zhaozhen
# @File : main.py
# @Software: PyCharm

import socket
from core.user_auth import UserOperation
from core.ftp_client import FilePutGet

sk = socket.socket()
sk.connect(('127.0.0.1',9050))

def choose_mune(opt_lst):
    try:
        # 显示可现在的操作
        for index, opt in enumerate(opt_lst, 1):
            print('\t{}、{}'.format(index, opt[0]))
        print('#'*24)
        # 选择操作
        num = int(input("请输入操作序号："))
        func = opt_lst[num - 1][1]
        return func
    except:
        pass

def main():
    while True:
        print("\033[1;31;46mFTP系统首页\033[0m".center(35, "#"))
        opt_lst = [('用户登录', 'login'), ('用户注册', 'register'), ('退出FTP程序', 'quit')]
        # 接受返回值
        func = choose_mune(opt_lst)
        try:
            # 判断是否有此功能
            if hasattr(UserOperation, func):
                # 调用此功能并接受返回值
                ret = getattr(UserOperation, func)(sk)
                while ret:
                    print("\033[1;31;46mFTP操作页\033[0m".center(36, "#"))
                    opt_lst2 = [('文件上传', 'put'), ('文件下载', 'get'), ('文件查看', 'show_file'), ('退出', 'quit')]
                    # 接受返回值
                    func = choose_mune(opt_lst2)
                    # 如果func是quit就退出
                    if func == 'quit':
                        break
                    # 否则判断是否有此功能
                    elif hasattr(FilePutGet,func):
                        # 调用此功能
                        getattr(FilePutGet,func)(sk)
        except TypeError:
            print("\033[031m不存在的功能,请重新输入\033[0m")